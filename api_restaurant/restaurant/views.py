import random

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False)
    def random(self, request):
        restaurant = self.queryset[
            random.randrange(0, len(self.queryset))
        ]

        serializer = RestaurantSerializer(restaurant)

        return Response(serializer.data)
