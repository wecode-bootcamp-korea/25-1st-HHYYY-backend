import json

from django.views                           import View
from django.http                            import JsonResponse
from django.db.models                       import Q
from django.db.models.aggregates            import Count, Min

from products.models                        import Category, SubCategory, Product

class ProductView(View) :
    def get(self, request) :
        category_id     = request.GET.get('category')
        sub_category_id = request.GET.get('subcategory')
        sort            = request.GET.get('sort')
        search          = request.GET.get('search')
        limit           = int(request.GET.get('limit', 0))
        offset          = int(request.GET.get('offset', 0))

        sort_list = {
            'low_price'  : 'price',
            'high_price' : '-price',
            'recent'     : '-created_at',
            'old'        : 'created_at',
            'review'     : '-review_count',
        }

        products_filter = Q(deleted_at = None)

        if category_id :
            products_filter.add(Q(sub_category__category = category_id), Q.AND)
        
        if sub_category_id :
            products_filter.add(Q(sub_category = sub_category_id), Q.AND)
        
        if search :
            products_filter.add(Q(name__icontains = search), Q.AND)
        
        products = Product.objects.filter(products_filter).prefetch_related('tags').annotate(price = Min('option__price'), review_count = Count('review')).order_by(sort_list.get(sort, 'id'))

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

        return JsonResponse({'DATA' : products_list}, status = 200)

class ProductDetailView(View) :
    def get(self, request, product_id) :
        if not Product.objects.filter(id = product_id).exists() :
            return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)
        
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

class CategoryView(View) :
    def get(self, request, category_id) :
        if not Category.objects.filter(id = category_id).exists() :
            return JsonResponse({'MESSAGE' : 'CATEGORY_DOES_NOT_EXIST'}, status = 404)
        
        category      = Category.objects.get(id = category_id)
        category_info = {
            'id'             : category.id,
            'name'           : category.name,
            'category_image' : category.image_url,
            'description'    : category.description,
        }

        return JsonResponse({'DATA' : category_info}, status = 200)

class SubCategoryView(View) :
    def get(self, request, subcategory_id) :
        if not SubCategory.objects.filter(id = subcategory_id).exists() :
            return JsonResponse({'MESSAGE' : 'SUBCATEGORY_DOES_NOT_EXIST'}, status = 404)
        
        sub_category      = SubCategory.objects.get(id = subcategory_id)
        sub_category_info = {
            'id'                 : sub_category.id,
            'name'               : sub_category.name,
            'sub_category_image' : sub_category.image_url,
            'description'        : sub_category.description,
        }

        return JsonResponse({'DATA' : sub_category_info}, status = 200)

class NavigatorView(View) :
    def get(self, request, category_id) :
        if not Category.objects.filter(id = category_id).exists() :
            return JsonResponse({'MESSAGE' : 'CATEGORY_DOES_NOT_EXIST'}, status = 404)
        
        category      = Category.objects.prefetch_related('subcategory_set__product_set').annotate(products_count = Count('subcategory__product')).get(id = category_id)
        category_list = {
            'category_id' : category.id,
            'category_name' : category.name,
            'category_products_count' : category.products_count,
            'sub_categories'          : [{
                'sub_category_id'             : sub_category.id,
                'sub_category_name'           : sub_category.name,
                'sub_category_products_count' : sub_category.product_set.count()
            } for sub_category in category.subcategory_set.all()]
        }

        return JsonResponse({'DATA' : category_list}, status = 200)