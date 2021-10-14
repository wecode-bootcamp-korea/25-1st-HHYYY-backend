from django.urls            import path

from products.views         import ProductView, ProductDetailView
from reviews.views          import ReviewView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/reviews/<int:product_id>', ReviewView.as_view()),
]