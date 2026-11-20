import unittest

from digital_product import DigitalProduct
from order import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from tests.helpers import make_product, make_supplier


class TestFactory(unittest.TestCase):
    def test_creates_physical_product(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, make_supplier(), weight=2.0)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertEqual(p.weight, 2.0)

    def test_creates_digital_product(self):
        p = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, make_supplier(), download_size=300.0)
        self.assertIsInstance(p, DigitalProduct)
        self.assertEqual(p.download_size, 300.0)

    def test_result_is_a_product(self):
        self.assertIsInstance(make_product(), Product)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, make_supplier())
        self.assertEqual(str(ctx.exception), "Unknown product type: service")


class TestValidation(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self):
        for bad in (0, -1, -0.01):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "X", bad, 1, make_supplier())

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "X", 10.0, -1, make_supplier())

    def test_zero_stock_is_allowed(self):
        self.assertEqual(ProductFactory.create("digital", "D1", "X", 10.0, 0, make_supplier()).stock, 0)

    def test_update_stock_rejects_negative_for_both_subclasses(self):
        # LSP: neither subclass may skip or change the parent's rule.
        for product_type in ("physical", "digital"):
            p = make_product(product_type=product_type)
            with self.assertRaises(ValueError):
                p.update_stock(-5)
            self.assertEqual(p.stock, 10)  # unchanged after the rejected update

    def test_price_setter_rejects_zero(self):
        p = make_product()
        with self.assertRaises(ValueError):
            p.price = 0

    def test_order_line_quantity_must_be_greater_than_zero(self):
        for bad in (0, -3):
            with self.assertRaises(ValueError) as ctx:
                OrderLine(make_product(), bad)
            self.assertEqual(str(ctx.exception), "Quantity must be greater than zero.")

    def test_order_line_protects_quantity_after_creation(self):
        line = OrderLine(make_product(), 2)
        with self.assertRaises(ValueError):
            line.quantity = 0
        self.assertEqual(line.quantity, 2)


if __name__ == "__main__":
    unittest.main()
