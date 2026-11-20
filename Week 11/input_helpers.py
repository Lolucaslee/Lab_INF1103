def get_positive_float(prompt: str) -> float:
    """
    Keeps asking until the user enters a number greater than zero.
    float() raises ValueError for text like 'abc'; the range rule is validation
    done with an if. Both lead to asking again.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keeps asking until the user enters a whole number that is 0 or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number that is 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")
