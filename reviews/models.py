from django.db              import models

from users.models           import User
from products.models        import Product

class Review(models.Model):
    user       = models.ForeignKey('users.User', on_delet = models.CASCADE)
    product    = models.ForeignKey('products.Product', on_delete = models.CASCADE)
    content    = models.CharField(max_length = 400)
    rating     = models.PositiveIntegerField()
    image_url  = models.CharField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'reviews'

class ReviewComment(models.Model):
    user       = models.ForeignKey('users.User', on_delet = models.CASCADE)
    review     = models.ForeignKey('Review', on_delete = models.CASCADE)
    content    = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.CharField(auto_now = True)
    
    class Meta:
        db_table = 'review_comments'

class ReviewLike(models.model):
    user   = models.ForeignKey('users.User', on_delete = models.CASCADE)
    review = models.ForeignKey('Review', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'review_likes'