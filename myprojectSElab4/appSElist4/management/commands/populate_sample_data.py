from django.core.management.base import BaseCommand
from appSElist4.models import Product, Customer, Order

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Xbox series s',price=999.00,
            available=True
        )

        product2 = Product.objects.create(
            name='PlayStation 5 pro', price=889.00,
            available=True
        )

        product3 = Product.objects.create(
            name='Nintendo Switch Plus', price=799.99,
            available=False
        )

        customer1 = Customer.objects.create(
            name='Lando Norris',
            address='Monaco Street 1'
        )

        customer2 = Customer.objects.create(
            name='Carlos Sainz',
            address='Barcelona Street 2'
        )

        customer3 = Customer.objects.create(
            name='Oscar Piastri',
            address='Melbourne Street 3'
        )

        order1 = Order.objects.create(
            customer=customer1, status='New')

        order1.products.add(product1, product2)

        order2 = Order.objects.create(
            customer=customer2, status='In Process')

        order2.products.add(product2)

        order3 = Order.objects.create(
            customer=customer3, status='Sent')

        order3.products.add(product3)


        self.stdout.write("Sample data created successfully.")
