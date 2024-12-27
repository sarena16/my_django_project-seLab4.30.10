from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from appSElist4.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ProductApiTest(APITestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')
        self.client = APIClient()

    def authenticate_regular_user(self):
        """ Helper method to authenticate with the regular user """
        self.token = str(AccessToken.for_user(self.regular_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def authenticate_admin_user(self):
        """ Helper method to authenticate with the admin user """
        self.token = str(AccessToken.for_user(self.admin))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_all_products_as_regular_user(self):
        self.authenticate_regular_user()

        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_all_products_as_admin(self):
        self.authenticate_admin_user()

        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_single_product_as_regular_user(self):
        self.authenticate_regular_user()

        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_get_single_product_as_admin(self):
        self.authenticate_admin_user()

        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_create_product_with_valid_data_as_regular_user(self):
        self.authenticate_regular_user()

        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_with_valid_data_as_admin(self):
        self.authenticate_admin_user()

        data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test cases for PATCH request (modify product)
    def test_modify_existing_product_as_regular_user(self):
        self.authenticate_regular_user()

        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_existing_product_as_admin(self):
        self.authenticate_admin_user()

        data = {"name": "Modified Product"}
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_as_regular_user(self):
        self.authenticate_regular_user()

        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_admin(self):
        self.authenticate_admin_user()

        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_product_with_invalid_data(self):
        self.authenticate_admin_user()

        data = {"name": "", "price": -4.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_non_existing_product(self):
        self.authenticate_admin_user()

        non_existing_url = reverse('product-detail', kwargs={'pk': 99999})
        response = self.client.get(non_existing_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_url(self):
        response = self.client.get('/invalid-url/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
