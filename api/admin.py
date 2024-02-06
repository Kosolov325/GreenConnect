from django.contrib import admin
from api.models.employee import *
from api.models.gift import *
from api.models.products import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(GiftType)
admin.site.register(Gift)
admin.site.register(GiftEntry)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductEntry)

