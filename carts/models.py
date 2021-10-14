from django.db                      import models

class Cart(models.Model) :
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)

    class Meta :
        db_table = 'carts'