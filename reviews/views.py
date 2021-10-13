import json

from django.views           import View
from django.http            import JsonResponse
from json.decoder           import JSONDecodeError

from reviews.models         import Review, ReviewComment, ReviewLike
from users.models           import User
from products.models        import Product
from users.decorators       import signin_decorator

class ReviewView(View):
    @signin_decorator
    def post(self, request, product_id):
        try:
            if not Product.objects.filter(id = product_id).exists() :
                return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)

            data   = json.loads(request.body)
            user   = request.user
            rating = int(data.get('rating'))

            if rating > 5 :
                return JsonResponse({'message' : 'INVALID_RATING'}, status = 400)

            Review.objects.create(
                user      = user,
                product   = Product.objects.get(id = product_id),
                content   = data.get('content'),
                rating    = rating,
                image_url = data.get('image_url')
            )
        
            return JsonResponse({'message':'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status = 400)

    @signin_decorator
    def get(self, request, product_id):
        try :
            if not Product.objects.filter(id = product_id).exists() :
                    return JsonResponse({'message' : 'INVALID_PRODUCT_ID'}, status = 404)
        
            product = Product.objects.get(id = product_id)
            limit   = int(request.GET.get('limit', 5))
            offset  = int(request.GET.get('offset', 0))

            reviews = Review.objects.filter(product = product).order_by('-created_at')
            
            if limit : 
                limit   = offset + limit
                reviews = reviews[offset : limit]
            
            review_list = [{
                'user_name'     : review.user.name,
                'content'       : review.content,
                'image'         : review.image_url,
                'rating'        : review.rating,
                'like_count'    : review.review_like_set.all().count(),
                'comment_count' : review.review_comment_set.all().count(),
                'created_at'    : review.created.at,
            } for review in reviews]

            return JsonResponse({'DATA' : review_list}, status = 200)
        
        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

class ReviewDetailView(View):
    @signin_decorator
    def delete(self, request, review_id):
        try:
            user = request.user
            if not Review.objects.filter(id=review_id).exists():
                return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status=404)

            review = Review.objects.get(id=review_id)

            if user.id != review.user.id :
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
        
            review.delete()

            return JsonResponse({'meassage' : 'SUCCESS'}, status = 201)
    
        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

    @signin_decorator
    def patch(self, request, review_id):
        try :
            user = request.user
            data = json.loads(request.body)
            if not Review.objects.filter(id=review_id).exists():
                return JsonResponse({'message' : 'INVALID_REIVEW_ID'}, status = 404)

            review = Review.objects.get(id=review_id)

            if user.id != review.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            review.content = data.get('content', review.content)
            review.rating  = data.get('rating', review.rating)
            review.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

    def get(self, request, review_id):
        try : 
            if not Review.objects.filter(id = review_id).exists():
                return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)

            review = Review.objects.get(id = review_id)

            review_info = {
                'user_name'    : review.user.name,
                'product_name' : review.product.name,
                'rating'       : review.rating,
                'image'        : review.image_url,
                'content'      : review.content,
                'like_count'   : review.review_like_set.all().count(),
            }

            return JsonResponse({'review_info' : review_info}, status = 200)

        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)
    

class ReviewCommentView(View):
    def get(self, request, review_id):
        
        if not Review.objects.filter(id = review_id).exists():
            return JsonResponse({'messages' : 'INVALID_REVIEW_ID'}, status = 404)

        comments_list = [{
            'user_name'    : comment.user.name,
            'content'      : comment.content,
            'created_at'   : comment.created_at,
        }for comment in ReviewComment.objects.filter(review_id = review_id) 
        ]

        return JsonResponse({'commnets_list' : comments_list }, status = 200)

    @signin_decorator
    def post(self, request, review_id):
        try :
            if not Review.objects.filter(id = review_id).exists() :
                return JsonResponse({'messages' : 'INVALID_REVIEW_ID'}, status = 404)

            data = json.loads(request.body)
            user = request.user

            ReviewComment.objects.create(
                user = user,
                review = Review.object.get(id = review_id),
                content = data.get('content'),
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)

    @signin_decorator
    def delete(self, request, comment_id):
        try :
            user = request.user
            if not ReviewComment.objects.filter(id = comment_id).exists() :
                return JsonResponse({'message' : 'INVALID_COMMENT_ID'}, status = 404)

            comment = ReviewComment.objects.get(id = comment_id)

            if user.id != comment.user :
                return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)

            comment.delete()

            return JsonResponse ({'message' : 'SUCCESS'}, status = 200)

        except ReviewComment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEWCOMMENT_ID'}, status = 404)
        
        except ReviewComment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400) 

    def patch(self, request, commnet_id):
        try :
            user = request.user
            data = json.loads(request.body)

            if not ReviewComment.objects.filter(id = commnet_id).exists() :
                return JsonResponse({'message' : 'INVALID_COMMNET_ID'}, status = 404)

            comment = ReviewComment.objects.get(id = commnet_id)

            if user.id != comment.user.id :
                return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)

            comment.content = data.get('commnet', comment.content)
            comment.save()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
        
        except ReviewComment.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEWCOMMENT_ID'}, status = 404)
        
        except ReviewComment.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)


class ReviewLikeView(View):
    @signin_decorator
    def post(self, request, review_id):
        try:
            user = request.user

            if not Review.objects.filter(id=review_id).exists():
                return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)

            review = Review.objects.get(id=review_id)

            if ReviewLike.objects.filter(user=user, review=review).exists():
                
                return JsonResponse({'message':'ALREADY_LIKE'}, status = 400)

            ReviewLike.objects.create(
                user=user,
                review=review
            )
            like_count = ReviewLike.objects.filter(review=review).count()

            return JsonResponse({'message' : 'SUCCESS', 'LIKE_COUNT' : like_count}, status = 200)

        except JSONDecodeError :
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

        except Review.DoesNotExist :
            return JsonResponse({'message' : 'INVALID_REVIEW_ID'}, status = 404)
        
        except Review.MultipleObjectsReturned :
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_ERROR'}, status = 400)