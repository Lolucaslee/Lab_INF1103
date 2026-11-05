from product import Product


class Inventory:
    """
    Manages collection of Product instances in an internal dictionary.
    Single Responsibility Principle (SRP): Maintains collection logic only.
    """

    def __init__(self):
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        """
        Adds a product to the internal collection.
        Returns True if successful, False if the Product ID already exists.
        """
        key = product.product_id.lower()
        if key in self._products:
            return False
        self._products[key] = product
        return True

    def search_product(self, product_id: str) -> Product | None:
        """Searches product by ID (case-insensitive). Returns Product or None."""
        return self._products.get(product_id.strip().lower())

    def display_all(self) -> None:
        """Loops through all stored products and invokes display_information()."""
        print("\nCurrent Inventory")
        if not self._products:
            print("No products in inventory.")
            return

        for product in self._products.values():
            product.display_information()

    def get_all_products(self) -> list[Product]:
        """Returns a list of all stored Product instances."""
        return list(self._products.values())