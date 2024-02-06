from api.gifts import GiftTypeViewSet, GiftEntryViewSet, GiftEntryViewSet, GiftEntryAddView, GiftValidate
from api.products import ProductTypeViewSet, ProductViewSet, ProductEntryViewSet, ProductEntryAddView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from api.auth import LoginAPIView, LogoutAPIView, RegisterAPIView
from api.employees import EmployeeViewSet
from django.urls import re_path, include
from rest_framework import routers

r1 = routers.DefaultRouter()
r1.register('employees', EmployeeViewSet, basename='employees')
r1.register('products', ProductViewSet, basename='products')
r1.register('product/types', ProductTypeViewSet, basename='product_types')
r1.register('product/entries', ProductEntryViewSet, basename='product_entries')
r1.register('gifts', GiftEntryViewSet, basename='gifts')
r1.register('gift/types', GiftTypeViewSet, basename='gift_types')
r1.register('gift/entries', GiftEntryViewSet, basename='gift_entries')


urlpatterns = [
    re_path('', include(r1.urls)),
    re_path('token', TokenObtainPairView().as_view(), name='token'),
    re_path('login', LoginAPIView().as_view(), name='login'),
    re_path('logout', LogoutAPIView.as_view(), name='logout'),
    re_path('register', RegisterAPIView.as_view(), name='register'),
    re_path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('product/entry/add', ProductEntryAddView.as_view(), name='product_entry_add'),
    re_path('gift/entry/add', GiftEntryAddView.as_view(), name='gift_entry_add'),
    re_path('gift/validate', GiftValidate.as_view(), name='gift_validate')
    
] 
