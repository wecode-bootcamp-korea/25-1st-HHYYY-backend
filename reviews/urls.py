from django.urls import path

from reviews.views import ReviewDetailView, ReviewLikeView, ReviewCommentView, ReviewCommentDetailView

urlpatterns = [
    path('/<int:review_id>', ReviewDetailView.as_view()),
    path('/comments/<int:review_id>', ReviewCommentView.as_view()),
    path('/comment/<int:comment_id>', ReviewCommentDetailView.as_view()),
    path('/like/<int:review_id>', ReviewLikeView.as_view()),
]