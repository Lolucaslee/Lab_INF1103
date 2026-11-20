import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """
    Reads products from a CSV file (header: product_type,product_id,name,
    price,stock_quantity), builds each through ProductFactory and adds it to
    the inventory.

    try     - open the file
    except  - FileNotFoundError: simple message, no crash
    else    - runs only if the file opened: read the rows
    finally - always runs
    One bad row is reported and skipped; loading carries on.
    """
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type.strip(),
                        product_id.strip(),
                        name.strip(),
                        float(price),
                        int(stock),
                        supplier,
                    )
                    if not inventory.add_product(product):
                        raise ValueError(f"duplicate product ID '{product_id.strip()}'")
                    loaded += 1
                except ValueError as err:
                    print(f"Skipping line {line_number}: {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
