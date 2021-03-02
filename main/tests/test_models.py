from decimal import Decimal
from django.test import TestCase
from main import models, factories
from main.models import Product


class TestModel(TestCase):
    #     def test_active_manager_works(self):
    #         models.Product.objects.create(
    #             name="The Cathedral and bazaar",
    #             price=Decimal("10.00"))
    #         models.Product.objects.create(
    #             name="Pride and Prejudice",
    #             price=Decimal('2.00'))
    #         models.Product.objects.create(
    #             name="A tale of Two cities",
    #             price=Decimal('2.00'),
    #             active=False,
    #         )
    #         self.assertEqual(len(models.Product.objects.active()), 2)

    # def test_create_order_works(self):
    #     p1 = models.Product.objects.create(
    #         name='Rich dad poor dad',
    #         price=Decimal('12.00'),
    #     )
    #     p2 = models.Product.objects.create(
    #         name='River and source',
    #         price=Decimal('34.00'),
    #     )
    #     user1 = models.User.objects.create_user('user1', 'test123')
    #     billing = models.Address.objects.create(
    #         user=user1,
    #         name='John Doe',
    #         address1='kk-37',
    #         city='Kakamega',
    #         country='Kenya',
    #     )
    #     shipping = models.Address.objects.create(
    #         user=user1,
    #         name='James Doe',
    #         address1='nk-37',
    #         city='Nyahururu',
    #         country='Kenya',
    #     )
    #     basket = models.Basket.objects.create(user=user1)
    #     models.BasketLine.objects.create(basket=basket, product=p2)
    #
    #     with self.assertLogs('main.models', level='INFO') as cm:
    #         order = basket.create_order(billing, shipping)
    #
    #     self.assertGreaterEqual(len(cm.output), 1)
    #     order.refresh_from_db()
    #     self.assertEquals(order.user, user1)
    #     self.assertEquals(order.billing_address1, 'kk-37')
    #     self.assertEquals(order.shipping_address1, 'nk-37')
    #     self.assertEquals(order.lines.all().count(), 2)
    #     lines = order.lines.all()
    #     self.assertEquals(lines[0].product, p1)
    #     self.assertEquals(lines[1].product, p2)

    def test_active_manager_works(self):
        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)
        self.assertEquals(len(models.Product.objects.active()), 2)

    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()
        user1 = factories.UserFactory()
        user2 = factories.UserFactory()
        billing1 = factories.AddressFactory(user=user1)
        shipping1 = factories.AddressFactory(user=user1)
        billing2 = factories.AddressFactory(user=user2)
        shipping2 = factories.AddressFactory(user=user2)

        basket1 = models.Basket.objects.create(user=user1)
        basket2 = models.Basket.objects.create(user=user2)
        models.BasketLine.objects.create(basket=basket1, product=p1)
        models.BasketLine.objects.create(basket=basket2, product=p2)

        with self.assertLogs('main.models', level='INFO') as cm:
            order1 = basket1.create_order(billing1, shipping1)
            order2 = basket2.create_order(billing2, shipping2)

        self.assertGreaterEqual(len(cm.output), 1)

        order1.refresh_from_db()
        order2.refresh_from_db()

        self.assertEquals(order1.user, user1)
        self.assertEquals(order1.billing_address1, billing1.address1)
        self.assertEquals(order1.lines.all().count(), 1)
        lines = order1.lines.all()
        print(lines)
        self.assertEquals(lines[0].product, p1)
        # self.assertEquals(lines[1].product, p2)
