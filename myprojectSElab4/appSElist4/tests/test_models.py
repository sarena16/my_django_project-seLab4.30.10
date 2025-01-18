from django.test import TestCase
from appSElist4.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            product = Product.objects.create(name='Negative Price', price=-1.99, available=True)
            product.full_clean()

    def test_create_product_without_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_without_availability(self):
        temp_product = Product.objects.create(name="Product without availability", price=10.00)
        self.assertFalse(temp_product.available)

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            product = Product.objects.create(name='Invalid Price Format', price=1.999, available=True)
            product.full_clean()

    def test_create_product_without_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Product without price', available=True)
            temp_product.full_clean()
            temp_product.save()

    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name=' ', price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_edge_name_length(self):
        max_length_name = 'a' * 150
        product = Product.objects.create(name=max_length_name, price=1.99, available=True)
        self.assertEqual(product.name, max_length_name)

        with self.assertRaises(ValidationError):
            too_long_name = 'a' * 151
            product = Product(name=too_long_name, price=1.99, available=True)
            product.full_clean()

    def test_create_product_with_edge_price_values(self):
        min_price = 0.01
        product = Product.objects.create(name='Min Price', price=min_price, available=True)
        self.assertEqual(product.price, min_price)

        max_price = 99999999.99
        product = Product.objects.create(name='Max Price', price=max_price, available=True)
        self.assertEqual(product.price, max_price)

        with self.assertRaises(ValidationError):
            product = Product(name='Invalid Min Price', price=0.009, available=True)
            product.full_clean()

        with self.assertRaises(ValidationError):
            product = Product(name='Invalid Max Price', price=100000000.00,
                              available=True)
            product.full_clean()





class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(name='Danny Ric', address='Melbourne Blvd')
        self.assertEqual(customer.name, 'Danny Ric')
        self.assertEqual(customer.address, 'Melbourne Blvd')

    def test_create_customer_without_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address='123 Main St')
            customer.full_clean()

    def test_create_customer_without_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='Danny Ric', address='')
            customer.full_clean()

    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name=None, address='Melbourne Blvd')
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='Danny Ric', address=None)
            customer.full_clean()

    def test_create_customer_with_edge_name_length(self):
        max_length_name = 'a' * 100
        customer = Customer.objects.create(name=max_length_name, address='Melbourne Blvd')
        self.assertEqual(customer.name, max_length_name)

        with self.assertRaises(ValidationError):
            too_long_name = 'a' * 101
            customer = Customer(name=too_long_name, address='Melbourne Blvd')
            customer.full_clean()

class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name='Daniel Riccardo', address='Melbourne Blvd')
        self.product1 = Product.objects.create(name='Product 1', price=10.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, available=False)

    def test_order_creation_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'New')
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())

    def test_order_creation_without_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(status='New')
            order.full_clean()

    def test_order_creation_without_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer)
            order.full_clean()

    def test_order_creation_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status='Invalid Status')
            order.full_clean()

    def test_total_price_calculation_with_valid_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.total_price(), 30.00)

    def test_total_price_calculation_with_no_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        self.assertEqual(order.total_price(), 0.00)

    def test_if_order_can_be_fulfilled_with_all_products_available(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        self.assertTrue(order.if_can_be_fulfilled())

    def test_if_order_can_be_fulfilled_with_some_products_unavailable(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1, self.product2)
        self.assertFalse(order.if_can_be_fulfilled())

