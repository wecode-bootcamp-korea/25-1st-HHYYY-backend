from django.db import models

class Category(models.Model) :
    name        = models.CharField(max_length = 50)
    image_url   = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 300)

    class Meta :
        db_table = 'categories'

class SubCategory(models.Model) :
    category    = models.ForeignKey('Category', on_delete = models.CASCADE)
    name        = models.CharField(max_length = 50)
    image_url   = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 300)

    class Meta :
        db_table = 'sub_categories'

class Product(models.Model) :
    sub_category  = models.ForeignKey('SubCategory', on_delete = models.PROTECT)
    tag           = models.ManyToManyField('Tag', through = 'ProductTag')
    name          = models.CharField(max_length = 50)
    thumbnail_url = models.CharField(max_length = 1000)
    created_at    = models.DateTimeField(auto_now_add = True)
    soft_delete   = models.BooleanField(default = False)

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
