from api.models.employee import Employee
from django.db import models


class ProductType(models.Model):
    name  = models.CharField(max_length=50)
    mnemo = models.CharField(max_length=10, db_index=True)
    
    class Meta:
        verbose_name = 'product type'
        verbose_name_plural = "Product types"
        db_table = "product_types"

    def __str__(self):
        return self.name

class Product(models.Model):
    label  = models.CharField(max_length=100)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'products'
        verbose_name_plural = "Products"
        db_table = "product_models"

    def __str__(self):
        return self.label
    
class ProductEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product entry'
        verbose_name_plural = "Product Entries"
        db_table = "product_entries"
    
    def __str__(self):
        return self.product.label