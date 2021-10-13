from django.db                      import models

from products.models                import Option
from users.models                   import User

class Cart(models.Model) :
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)

    class Meta :
        db_table = 'carts'