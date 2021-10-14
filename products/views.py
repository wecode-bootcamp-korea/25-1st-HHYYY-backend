import json

from django.views                           import View
from django.http                            import JsonResponse
from django.db.models                       import Q
from django.db.models.aggregates            import Avg, Count, Min
from django.db.models.query                 import Prefetch

from products.models                        import Category, Product
from reviews.models                         import Review

class Navigator :
    def __init__(self, category) :
        self.category = category
    
    def get_category(self) :
        category = self.category.main_category if self.category.main_category else self.category
        return category
    
    def gennerate_navigator_list(self) :
        navigator_list = {
            'category_id'                 : self.get_category().id,
            'category_name'               : self.get_category().name,
            'category_products_count'     : Product.objects.filter(category__main_category = self.get_category()).count(),
            'sub_categories'              : [{
            'sub_category_id'             : sub_category.id,
            'sub_category_name'           : sub_category.name,
            'sub_category_products_count' : sub_category.product_set.count()
            } for sub_category in self.get_category().sub_category.prefetch_related('product_set').all()]
            }

        return navigator_list

class ProductView(View) :
    def get(self, request) :
        try :
            category_id = request.GET.get('category')
            sort        = request.GET.get('sort')
            search      = request.GET.get('search')
            limit       = int(request.GET.get('limit', 0))
            offset      = int(request.GET.get('offset', 0))

            sort_by = {
                'low_price'  : 'price',
                'high_price' : '-price',
                'recent'     : '-created_at',
                'old'        : 'created_at',
                'review'     : '-review_count',
            }

            products_filter = Q(deleted_at = None)
            category_info   = {}

            if category_id :
                category = Category.objects.select_related('main_category').get(id = category_id)
                products_filter.add(Q(category = category) if category.main_category else Q(category__main_category = category), Q.AND)

                category_info = {
                    'id'             : category.id,
                    'name'           : category.name,
                    'category_image' : category.image_url,
                    'description'    : category.description,
                }

            if search :
                products_filter.add(Q(name__icontains = search)|Q(category__main_category__name = search)|Q(category__name = search), Q.AND)
        
            products = Product.objects.filter(products_filter).prefetch_related('tags').annotate(price = Min('option__price'), review_count = Count('review'))\
                       .order_by(sort_by.get(sort, 'id'))

            if limit :
                limit    = offset + limit
                products = products[offset : limit]

            products_list = [{
                'id'            : product.id,
                'name'          : product.name,
                'thumbnail_url' : product.thumbnail_url,
                'price'         : product.price,
                'tags'          : [tag.name for tag in product.tags.all()]
            } for product in products]

            products_count = len(products_list)

            return JsonResponse({'category_info' : category_info, 'products_list' : products_list, 'products_count' : products_count}, status = 200)
        
        except Category.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_CATEGORY_ID'}, status = 404)
        
        except Category.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_CATEGORY_ERROR'}, status = 400)

class ProductDetailView(View) :
    def get(self, request, product_id) :
        try :
            if not Product.objects.filter(id = product_id).exists() :
                return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)
        
            product = Product.objects.prefetch_related(
                     'option_set', 'tags', 'detailimage_set', Prefetch('review_set', queryset = Review.objects.filter(product = product_id).order_by('-created_at')))\
                      .select_related('category__main_category').annotate(rating_average = Avg('review__rating')).get(id = product_id)
            
            product_info = {
                'id'                 : product.id,
                'name'               : product.name,
                'thumbnail_url'      : product.thumbnail_url,
                'how_to'             : product.how_to,
                'ingredients'        : product.ingredients,
                'options'            : [{
                    'option_id'      : option.id,
                    'price'          : option.price,
                    'size'           : option.size,
                } for option in product.option_set.all()],
                'tags'               : [tag.name for tag in product.tags.all()],
                'main_category_name' : product.category.main_category.name,
                'sub_category_name'  : product.category.name,
                'detail_images'      : [image.image_url for image in product.detailimage_set.all()],
                'rating_average'     : round(product.rating_average, 1) if product.rating_average else 0,
                'review_count'       : product.review_set.count(),
                'photo_review_count' : len([review.image_url for review in product.review_set.all() if review.image_url]),
                'review_id'          : [review.id for review in product.review_set.all()][:4],
                'review_images'      : [review.image_url for review in product.review_set.all() if review.image_url][:4]
            }

            return JsonResponse({'product_info' : product_info}, status = 200)
        
        except Product.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)
        
        except Product.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_PRODUCT_ERROR'}, status = 400)

class NavigatorView(View) :
    def get(self, request, category_id) :
        try :
            if not Category.objects.filter(id = category_id).exists() :
                return JsonResponse({'message' : 'INVALID_CATEGORY_ID'}, status = 404)
         
            category       = Category.objects.select_related('main_category').get(id = category_id)
            navigator      = Navigator(category)
            navigator_list = navigator.gennerate_navigator_list()
            
            return JsonResponse({'navigator_list' : navigator_list}, status = 200)
        
        except Category.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_CATEGORY_ID'}, status = 404)
        
        except Category.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_CATEGORY_ERROR'}, status = 400)

class CategoryView(View) :
    def get(self, request) :
        categories     = Category.objects.all()
        
        category_list  = [{
            'category_id'   : category.id,
            'category_name' : category.name,
        } for category in categories]

        return JsonResponse({'category_list' : category_list})