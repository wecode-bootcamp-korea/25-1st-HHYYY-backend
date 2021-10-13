from django.urls import path

from reviews.views import ReviewDetailView, ReviewLikeView, ReviewView, ReviewCommentView  

urlpatterns = [
    path('/<int:product_id>', ReviewView.as_view()),
    path('/comment/<int:review_id>', ReviewCommentView.as_view()),
    path('/deatil<int:review_id>', ReviewDetailView.as_view()),
    path('/like<int:review_id>', ReviewLikeView.as_view())
]