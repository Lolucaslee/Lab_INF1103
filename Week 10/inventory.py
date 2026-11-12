from product import Product


class Inventory:
    """
    Manages a collection of Product references.

    Relationship: AGGREGATION with Product. The inventory holds references to
    products but does not create them or control their lifecycle; removing a
    product here does not destroy it.
    Works only with the Product abstraction (LSP) - never checks subclasses.
    """

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """
        Adds an existing Product object.
        Returns True if added, False if the Product ID already exists.
        """
        if self.find_product(product.product_id) is not None:
            return False
        self.products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """
        Removes the matching Product reference from this inventory.
        The Product itself is NOT destroyed; it is returned so it can be reused
        (e.g. added to another inventory). Returns None if not found.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Finds a product by ID (case-insensitive). Returns Product or None."""
        wanted = product_id.strip().lower()
        for product in self.products:
            if product.product_id.lower() == wanted:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        """Kept for backwards compatibility; same as find_product."""
        return self.find_product(product_id)

    def display_all(self) -> None:
        """Asks each Product to display itself (polymorphism)."""
        print("\nCurrent Inventory")
        if not self.products:
            print("No products in inventory.")
            return

        for product in self.products:
            product.display_information()

    def get_all_products(self) -> list[Product]:
        """Returns a copy of the list of stored Product references."""
        return list(self.products)
