class Supplier:
    """
    A supplier of products.

    Relationship: ASSOCIATION with Product. A Supplier is created independently
    and handed to a Product; neither owns the other and either can exist alone.
    """

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self._supplier_id: str = str(supplier_id)
        self._name: str = str(name)
        self._contact_email: str = str(contact_email)

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact_email(self) -> str:
        return self._contact_email

    def display_information(self) -> None:
        """Prints the supplier's details."""
        print(
            f"Supplier ID: {self._supplier_id} | Name: {self._name} "
            f"| Email: {self._contact_email}"
        )

    def to_dict(self) -> dict:
        """Dictionary form for JSON export."""
        return {
            "id": self._supplier_id,
            "name": self._name,
            "email": self._contact_email,
        }
