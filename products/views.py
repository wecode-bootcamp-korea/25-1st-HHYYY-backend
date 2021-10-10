import json

from django.views                           import View
from django.http                            import JsonResponse
from django.db.models                       import Q
from django.db.models.aggregates            import Count, Min

from products.models                        import Category, Product

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
            category_list   = {}

            if category_id :
                category = Category.objects.select_related('main_category').get(id = category_id)

                category_info = {
                    'id'             : category.id,
                    'name'           : category.name,
                    'category_image' : category.image_url,
                    'description'    : category.description,
                }

                if category.main_category == None :
                    products_filter.add(Q(category__main_category = category_id), Q.AND)

                    category_list = {
                        'category_id'                 : category.id,
                        'category_name'               : category.name,
                        'category_products_count'     : Product.objects.filter(category__main_category = category).count(),
                        'sub_categories'              : [{
                        'sub_category_id'             : sub_category.id,
                        'sub_category_name'           : sub_category.name,
                        'sub_category_products_count' : sub_category.product_set.count()
                        } for sub_category in category.sub_category.prefetch_related('product_set').all()]
                    }

                else :
                    products_filter.add((Q(category = category_id)), Q.AND)

                    category_list = {
                        'category_id'                 : category.main_category.id,
                        'category_name'               : category.main_category.name,
                        'category_products_count'     : Product.objects.filter(category__main_category = category.main_category).count(),
                        'sub_categories'              : [{
                        'sub_category_id'             : sub_category.id,
                        'sub_category_name'           : sub_category.name,
                        'sub_category_products_count' : sub_category.product_set.count()
                        } for sub_category in category.main_category.sub_category.prefetch_related('product_set').all()]
                    }
        
            if search :
                products_filter.add(Q(name__icontains = search)|Q(category__main_category__name__exact = search)|Q(category__name__exact = search), Q.AND)
        
            products = Product.objects.filter(products_filter).prefetch_related('tags').annotate(price = Min('option__price'), review_count = Count('review'))\
                       .order_by(sort_by.get(sort, 'id'))

            if limit :
                limit    = offset + limit
                products = products[offset : limit]

            products_list = [{
                'id'            : product.id,
                'name'          : product.name,
                'thumnbail_url' : product.thumbnail_url,
                'price'         : product.price,
                'tags'          : [tag.name for tag in product.tags.all()]
            } for product in products]

            return JsonResponse({'category_info' : category_info, 'category_list' : category_list, 'products_list' : products_list}, status = 200)
        
        except Category.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_CATEGORY_ID'}, status = 404)
        
        except Category.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_CATEGORY_ERROR'}, status = 400)

class ProductDetailView(View) :
    def get(self, request, product_id) :
        try :
            if not Product.objects.filter(id = product_id).exists() :
                return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)
        
            product      = Product.objects.prefetch_related('option_set', 'tags', 'detailimage_set').get(id = product_id)
            product_info = {
                'id'            : product.id,
                'name'          : product.name,
                'thumbnail_url' : product.thumbnail_url,
                'options'       : [{
                    'option_id' : option.id,
                    'price'     : option.price,
                    'size'      : option.size,
                } for option in product.option_set.all()],
                'tags'          : [tag.name for tag in product.tags.all()],
                'detail_images' : [image.image_url for image in product.detailimage_set.all()]
            }

            return JsonResponse({'DATA' : product_info}, status = 200)
        
        except Product.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)
        
        except Product.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_PRODUCT_ERROR'}, status = 400)