from django.test import TestCase, Client
from rest_framework import status
from .models import Item


class HealthCheckTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check(self):
        """Test health check endpoint returns 200 OK"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'ok')


class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.item = Item.objects.create(
            name='Test Item',
            description='Test Description',
            quantity=10
        )

    def test_list_items(self):
        """Test listing all items"""
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('items', data)
        self.assertEqual(len(data['items']), 1)

    def test_create_item(self):
        """Test creating a new item"""
        data = {
            'name': 'New Item',
            'description': 'New Description',
            'quantity': 5
        }
        response = self.client.post(
            '/api/items/',
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

    def test_get_item_detail(self):
        """Test retrieving item details"""
        response = self.client.get(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['name'], 'Test Item')

    def test_update_item(self):
        """Test updating an item"""
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'quantity': 20
        }
        response = self.client.put(
            f'/api/items/{self.item.id}/',
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')

    def test_delete_item(self):
        """Test deleting an item"""
        response = self.client.delete(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_get_nonexistent_item(self):
        """Test retrieving a non-existent item returns 404"""
        response = self.client.get('/api/items/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MetricsExampleTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_metrics_example(self):
        """Test metrics example endpoint"""
        response = self.client.get('/api/metrics-example/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('_cerberus_metrics', data)

    def test_error_endpoint(self):
        """Test error example endpoint"""
        response = self.client.get('/api/error/?type=validation')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
