import json

from django.views                           import View
from django.http                            import JsonResponse
from django.db.models                       import Sum, F
from json.decoder                           import JSONDecodeError

from carts.models                           import Cart
from products.models                        import Option
# 로그인 데코레이터 지훈님 브랜치에 있어서 추후 import 예정

class CartView(View) :
    @login_decorator
    def post(self, request):
        try :
            data      = json.loads(request.body)
            user      = request.user
            option_id = data['option_id']
            quantity  = int(data['quantity'])

            if not Option.objects.filter(id = option_id).exists():
                return JsonResponse({'message' : 'INVALID_OPTION_ID'}, status = 404)
               
            cart, created = Cart.objects.get_or_create(
                user = user,
                option_id = option_id
            )

            cart.quantity += quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
       
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
        
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status = 400)
    
    @login_decorator
    def get(self, request):
        FREE_SHIPPING = 30000
        SHIPPING      = 2500
        carts         = Cart.objects.filter(user = request.user).select_related('option__product__category')

        cart_list = [{
            'cart_id'       : item.id,
            'product_id'    : item.option.product.id,
            'product_name'  : item.option.product.name,
            'category_name' : item.option.product.category.name,
            'size'          : item.option.size,
            'quantity'      : item.quantity,
            'product_price' : item.option.price,
            'product_image' : item.option.product.thumbnail_url,
            'price'         : int(item.option.price) * int(item.quantity)
        }for item in carts]

        total_price    = int(carts.aggregate(total = Sum(F('quantity')*F('option__price')))['total'] or 0)
        shipping_price = 0 if total_price >= FREE_SHIPPING else SHIPPING
        order_price    = total_price + shipping_price

        return JsonResponse({
            'cart_list'   : cart_list,
            'total_price' : total_price,
            'shipping'    : shipping_price,
            'order_price' : order_price,
        }, status = 200)

class CartDetailView(View):
    @login_decorator
    def delete(self, request, cart_id):
        try : 
            if not Cart.objects.filter(id = cart_id, user = request.user).exists():
                return JsonResponse({'message' : 'INVALID_CART_ID'}, status = 404)
            
            item = Cart.objects.get(id = cart_id, user = request.user)
            item.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART_ID'}, status = 404)
        
        except Cart.MultipleObjectsReturned:
            return JsonResponse({'message' : 'MULTIPLE_CART_ERROR'}, status = 400)
    
    @login_decorator
    def patch(self, request, cart_id):
        try :
            if not Cart.objects.filter(id = cart_id, user = request.user).exists():
                return JsonResponse({'message' : 'INVALID_CART_ID'}, status = 404)
            
            data          = json.loads(request.body)
            item          = Cart.objects.get(id = cart_id, user = request.user)
            item.quantity = int(data.get('quantity', item.quantity))
            item.save()

            return JsonResponse({'message' : 'SUCCESS', 'quantity' : item.quantity}, status = 200)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART_ID'}, status = 404)
        
        except Cart.MultipleObjectsReturned:
            return JsonResponse({'message' : 'MULTIPLE_CART_ERROR'}, status = 400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'})


