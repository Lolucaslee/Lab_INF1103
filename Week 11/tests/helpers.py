from product_factory import ProductFactory
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSupply Co", "sales@techsupply.com")


def make_product(product_id: str = "P001", price: float = 100.0, product_type: str = "physical"):
    """Builds a product the way the program should: through the factory."""
    return ProductFactory.create(product_type, product_id, "Item " + product_id, price, 10, make_supplier())
