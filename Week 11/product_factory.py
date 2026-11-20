from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """
    Factory pattern: the ONE place that knows which concrete product class to
    build. The rest of the program asks for a Product and only deals with the
    Product type (polymorphism). It creates products but does not store them.
    """

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        **extra: float,
    ) -> Product:
        """
        Builds a product of the requested type.
        extra may hold 'weight' (physical) or 'download_size' (digital);
        each defaults to 0.0 when not given (e.g. from a CSV file).
        Raises ValueError for an unknown product type.
        """
        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier,
                extra.get("weight", 0.0),
            )
        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, supplier,
                extra.get("download_size", 0.0),
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")
