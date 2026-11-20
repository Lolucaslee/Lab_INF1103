import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from input_helpers import get_non_negative_int, get_positive_float
from inventory import Inventory
from product_loader import load_products
from tests.helpers import make_supplier

CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


def run_quietly(func, *args):
    """Runs func, returning (result, printed output)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestInputHelpers(unittest.TestCase):
    def test_asks_again_until_valid_price(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            value, out = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(
            out.strip().splitlines(),
            ["Please enter a valid number, e.g. 12.50", "Please enter a number greater than zero."],
        )

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]):
            value, _ = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 3.0)

    def test_non_negative_int_asks_again(self):
        with patch("builtins.input", side_effect=["x", "-1", "2.5", "7"]):
            value, _ = run_quietly(get_non_negative_int, "Stock: ")
        self.assertEqual(value, 7)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "products.csv")
        with open(self.path, "w", newline="") as f:
            f.write(CSV_TEXT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        inv = Inventory()
        _, out = run_quietly(load_products, self.path, inv, make_supplier())
        self.assertEqual({p.product_id for p in inv.products}, {"P001", "D001", "P003"})
        self.assertIn("3 products loaded.", out)

    def test_bad_rows_are_reported(self):
        _, out = run_quietly(load_products, self.path, Inventory(), make_supplier())
        self.assertIn("Unknown product type: service", out)
        self.assertIn("could not convert string to float", out)

    def test_message_order(self):
        _, out = run_quietly(load_products, self.path, Inventory(), make_supplier())
        lines = out.strip().splitlines()
        self.assertTrue(lines[0].startswith("Skipping line 4"))
        self.assertTrue(lines[1].startswith("Skipping line 5"))
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_without_crashing(self):
        inv = Inventory()
        missing = os.path.join(self.tmp.name, "nope.csv")
        _, out = run_quietly(load_products, missing, inv, make_supplier())
        self.assertEqual(inv.products, [])
        self.assertEqual(
            out.strip().splitlines(),
            [f"Products file not found: {missing}", "Load attempt finished."],
        )
        self.assertNotIn("products loaded", out)  # the else block did not run

    def test_duplicate_id_row_is_skipped(self):
        inv = Inventory()
        run_quietly(load_products, self.path, inv, make_supplier())
        _, out = run_quietly(load_products, self.path, inv, make_supplier())
        self.assertIn("duplicate product ID", out)
        self.assertIn("0 products loaded.", out)


if __name__ == "__main__":
    unittest.main()
