from django.urls            import path

from products.views         import ProductView, ProductDetailView, NavigatorView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/navigator/<int:category_id>', NavigatorView.as_view())
]