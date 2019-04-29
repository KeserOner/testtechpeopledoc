from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantRessourceTest(APITestCase):
    """Our class for tests. Use data migrations for datas."""

    client = APIClient()

    def test_list_restaurants(self):
        response = self.client.get(reverse('restaurant-list'))

        right_output = Restaurant.objects.all()
        serialized_out = RestaurantSerializer(right_output, many=True)
        self.assertEqual(response.data, serialized_out.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant(self):
        response = self.client.get(
            reverse('restaurant-detail', kwargs={'pk': 1})
        )

        right_output = Restaurant.objects.get(pk=1)
        serialized_out = RestaurantSerializer(right_output)
        self.assertEqual(response.data, serialized_out.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_restaurant(self):
        data = {'name': 'foo', 'city': 'bar'}
        old_qs = Restaurant.objects.all()
        response = self.client.post(
            reverse('restaurant-list'),
            data,
            format='json'
        )

        new_qs = Restaurant.objects.all()
        self.assertNotEqual(old_qs, new_qs)
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_random_restaurant(self):
        response = self.client.get(reverse('restaurant-random'))

        self.assertIn('city', response.data)
        restaurant = Restaurant.objects.filter(city=response.data['city'])
        self.assertEqual(len(restaurant), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_restaurant(self):
        old_qs = Restaurant.objects.all()
        response = self.client.delete(
            reverse('restaurant-detail', kwargs={'pk': 3})
        )

        new_qs = Restaurant.objects.all()
        self.assertNotEqual(old_qs, new_qs)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_restaurant(self):
        data = {'name': 'Green Goose', 'city': 'Paris 11'}
        response = self.client.patch(
            reverse('restaurant-detail', kwargs={'pk': 1}),
            data,
            format='json'
        )

        update = Restaurant.objects.get(pk=1)
        empty = Restaurant.objects.filter(city='Paris')
        self.assertFalse(empty)
        self.assertEqual(update.city, 'Paris 11')
        self.assertEqual(update.name, 'Green Goose')
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_restaurant(self):
        data = {'name': 'Red Goose', 'city': 'Paris'}
        response = self.client.put(
            reverse('restaurant-detail', kwargs={'pk': 1}),
            data,
            format='json'
        )

        update = Restaurant.objects.get(pk=1)
        empty = Restaurant.objects.filter(name='Green Goose')
        self.assertFalse(empty)
        self.assertEqual(update.city, 'Paris')
        self.assertEqual(update.name, 'Red Goose')
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
