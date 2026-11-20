FROM python:3.11-slim

WORKDIR /APP

# Copy all python source files, the sample CSV, the data file and the tests
COPY *.py .
COPY products.csv .
COPY inventory.json .
COPY tests/ tests/

# Default: run the program. To run the automated tests instead:
#   docker run <image> python -m unittest discover -s tests -t .
CMD ["python", "inventory_manager.py"]
