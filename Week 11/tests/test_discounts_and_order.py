import inspect
import unittest

import order
from discount import (BulkDiscount, DiscountStrategy, NoDiscount,
                      PercentageDiscount, StudentDiscount)
from order import Order
from tests.helpers import make_product


class TestStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150.0), 150.0)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(100.0), 95.0)

    def test_all_strategies_share_the_base_class(self):
        for strategy in (NoDiscount(), PercentageDiscount(5), BulkDiscount(1, 1), StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)

    def test_base_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()  # type: ignore

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


class TestOrderUsesStrategy(unittest.TestCase):
    def make_order(self, discount=None) -> Order:
        o = Order("O1", discount)
        o.add_order_line(make_product("P1", 100.0), 2)
        o.add_order_line(make_product("P2", 50.0), 1)  # lines add up to 250
        return o

    def test_default_is_no_discount(self):
        self.assertEqual(self.make_order().calculate_total(), 250.0)

    def test_bulk_discount_via_order(self):
        self.assertEqual(self.make_order(BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self):
        o = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(o.calculate_total(), 230.0)
        o.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(o.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self):
        # StudentDiscount was added after Order was written; Order is unchanged.
        self.assertAlmostEqual(self.make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_order_source_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(order.Order.calculate_total)
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)
        self.assertNotIn("percentage", source.lower())

    def test_two_orders_can_share_one_strategy_object(self):
        shared = PercentageDiscount(10)
        a, b = self.make_order(shared), self.make_order(shared)
        self.assertIs(a.discount, b.discount)


if __name__ == "__main__":
    unittest.main()
