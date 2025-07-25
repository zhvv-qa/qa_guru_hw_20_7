"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(400) is True  # достаточно товара
        assert product.check_quantity(1000) is True  # ровно столько, сколько есть
        assert product.check_quantity(1001) is False  # больше, чем есть
        assert product.check_quantity(0) is True  # запрос на 0 товара должен быть допустим

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(300)
        assert product.quantity == 700  # проверка, что количество уменьшилось

        product.buy(700)
        assert product.quantity == 0  # проверка, что купили всё

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):  # указываем, что ожидаем ValueError
            product.buy(1500)  # попытка купить больше, чем есть в наличии


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        """
        Проверяем, что продукт добавляется в корзину
        """
        cart.add_product(product, 2)  # добавить 2 продукта в корзину
        assert product in cart.products  # проверка, что продукт есть в корзине
        assert cart.products[product] == 2  # проверка, что количество продуктов в корзине соответствует добавленному

    def test_add_product_already_in_cart(self, cart, product):
        """
        Проверяем, что при добавлении продукта, который уже есть в корзине, количество увеличивается
        """
        cart.add_product(product, 1)
        cart.add_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product(self, cart, product):
        """
        Проверяем, что продукт удаляется из корзины
        """
        cart.add_product(product, 3)
        cart.remove_product(product, 2)
        assert cart.products[product] == 1 # проверка, что количество уменьшилось на 2

    def test_remove_product_completely(self, cart, product):
        """
        Проверяем, что продукт полностью удаляется из корзины, если удалить все
        """
        cart.add_product(product, 1)
        cart.remove_product(product, 1)
        assert product not in cart.products  # проверка, что продукта нет в корзине

    def test_clear(self, cart, product):
        """
        Проверяем, что корзина очищается полностью
        """
        cart.add_product(product, 2)
        cart.clear()
        assert not cart.products

    def test_get_total_price(self, cart, product):
        """
        Проверяем, что общая стоимость корзины рассчитывается верно
        """
        cart.add_product(product, 2)
        assert cart.get_total_price() == product.price * 2

    def test_buy(self, cart, product):
        """
        Проверяем, что метод buy уменьшает количество продукта на складе и очищает корзину
        """
        cart.add_product(product, 2)
        cart.buy()
        assert product.quantity == 998
        assert not cart.products

    def test_buy_not_enough_product(self, cart, product):
        """
        Проверяем, что если на складе не хватает товара, то выбрасывается исключение
        """
        cart.add_product(product, 1001)  # попытка купить больше, чем есть на складе
        with pytest.raises(ValueError, match="Недостаточно товара на складе"):
            cart.buy()
