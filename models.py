class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return self.quantity >= quantity  # проверка достаточно ли товара

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if not self.check_quantity(quantity):   # достаточно ли товара
            raise ValueError("Недостаточно товара на складе")  # если товара недостаточно, вызов исключения
        self.quantity -= quantity   # уменьшаем количество товара на складе -=

    def __hash__(self):
        return hash(self.name + self.description)  # возвращает целое число, которое является хеш-кодом товара по name и description

class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:   # проверка есть ли такой продукт в корзине
            self.products[product] += buy_count  # если продукт есть, увеличиваем количество
        else:
            self.products[product] = buy_count   # если продукта нет, то добавить в корзину

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:   # проверка есть ли продукт в корзине
            if remove_count is None or remove_count >= self.products[product]:   # нужно ли удалять всю позицию товара
                del self.products[product]   # если нужно удалить всю позицию, то удалить из словаря self.products
            else:
                self.products[product] -= remove_count   # если remove_count был передан и он меньше, чем количество
                                                         # товара в позиции, то уменьшить количество товара

    def clear(self):
        self.products = {}   # очистить корзину

    def get_total_price(self) -> float:   # возвращает общую стоимость товаров в корзине
        total_price = 0.0
        for product, quantity in self.products.items():
            total_price += product.price * quantity
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, quantity in self.products.items():   # перебираем товары в корзине
            if not product.check_quantity(quantity):   # проверка наличия товара на складе
                raise ValueError(f"Недостаточно товара на складе для: {product.name}")   # если товара не хватает, вызов исключения

        for product, quantity in self.products.items():   # перебираем товары в корзине
            product.buy(quantity)  # используем метод buy из Product, чтобы уменьшить количество товара на складе
        self.clear()   # очистить корзину