from product import Product


class Inventory:
    """
    Manages a collection of Product instances.
    
    Responsibility (SRP):
    Maintains the product collection, adding, searching, and displaying items.
    """

    def __init__(self):
        # Internal dictionary mapping product_id (case-insensitive) -> Product object
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        """
        Adds a product to the collection if the ID does not already exist.
        Returns True if successful, False if duplicate ID.
        """
        key = product.product_id.lower()
        if key in self._products:
            return False
        self._products[key] = product
        return True

    def search_product(self, product_id: str) -> Product | None:
        """
        Searches for a product by ID (case-insensitive).
        Returns the Product object if found, or None.
        """
        return self._products.get(product_id.strip().lower())

    def display_all(self) -> None:
        """Displays all products using exact layout from Week 5."""
        print("\nCurrent Inventory")
        if not self._products:
            print("No products in inventory.")
            return

        for product in self._products.values():
            product.display_information()

    def get_all_products(self) -> list[Product]:
        """Returns list of all stored Product objects."""
        return list(self._products.values())