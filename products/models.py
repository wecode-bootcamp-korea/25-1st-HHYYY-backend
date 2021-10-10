from django.db import models
from django.db.models.deletion import CASCADE

class Category(models.Model) :
    name            = models.CharField(max_length = 50)
    image_url       = models.CharField(max_length = 1000)
    description     = models.CharField(max_length = 300)
    main_category   = models.ForeignKey('self', on_delete = models.CASCADE, null = True, related_name = 'sub_category')

    class Meta :
        db_table = 'categories'

class Product(models.Model) :
    category      = models.ForeignKey('Category', on_delete = CASCADE)
    tags          = models.ManyToManyField('Tag', through = 'ProductTag')
    name          = models.CharField(max_length = 50)
    thumbnail_url = models.CharField(max_length = 1000)
    how_to        = models.CharField(max_length = 2000, null = True, default = None)
    ingredients   = models.CharField(max_length = 2000, null = True, default = None)
    created_at    = models.DateTimeField(auto_now_add = True)
    deleted_at    = models.DateTimeField(null = True, default = None)

    class Meta :
        db_table = 'products'

class Option(models.Model) :
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    price   = models.PositiveIntegerField()
    size    = models.PositiveIntegerField()

    class Meta :
        db_table = 'options'

class DetailImage(models.Model) :
    product   = models.ForeignKey('Product', on_delete = models.CASCADE)
    image_url = models.CharField(max_length = 1000)

    class Meta :
        db_table = 'detail_images'

class Tag(models.Model) :
    name = models.CharField(max_length = 50)

    class Meta :
        db_table = 'tags'

class ProductTag(models.Model):
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    tag     = models.ForeignKey('Tag', on_delete = models.CASCADE)

    class Meta:
        db_table = 'products_tags'
