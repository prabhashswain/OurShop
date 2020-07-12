from django.db import models
from .category import Category

class Product(models.Model):
    name        = models.CharField(max_length=30)
    price       = models.IntegerField(default=0)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=200,null=True,blank=True)
    image       = models.ImageField(upload_to='product/')
    
    def delete(self,*args,**kwargs):
        self.image.delete()
        super().delete(*args,**kwargs)
        
    @staticmethod
    def get_product_by_ids(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_categoryid(category_id):
        return Product.objects.filter(category=category_id)

    def __str__(self):
        return self.name    