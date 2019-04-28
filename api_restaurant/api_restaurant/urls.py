from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from restaurant.views import RestaurantViewSet

router = routers.SimpleRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
