
import requests
import unittest

def list_datasets(limit=None):
    """Fetch a list of available datasets from the Chicago Data Portal."""
    url = "https://data.cityofchicago.org/api/catalog/v1"
    if limit is not None:
        params = {"limit": limit}
    else:
        params = {}

    response = requests.get(url, params=params)
    response.raise_for_status()

    datasets = response.json().get("results", [])
    return datasets

# Example usage for unittest
# datasets = list_datasets(limit=5)
# for i, ds in enumerate(datasets, 1):
#    print(f"{i}. {ds['name']} (ID: {ds['resource']['id']}) - {ds['description']}")

def search_datasets(query, limit=None):
    """Search datasets by keyword (e.g., 'crime', 'business', 'transport')."""
    url = "https://data.cityofchicago.org/api/catalog/v1"
    if limit is not None:
        params = {"q": query, "limit": limit}
    else:
        params = {"q": query}

    response = requests.get(url, params=params)
    response.raise_for_status()

    results = response.json().get("results", [])
    return results

# # Example: Search for crime-related datasets
# crime_datasets = search_datasets("crime", limit=5)
# for ds in crime_datasets:
#     print(f"{ds['name']} (ID: {ds['resource']['id']}) - {ds['description']}")

def get_dataset_metadata(dataset_id):
    """Fetch metadata for a specific dataset."""
    url = f"https://data.cityofchicago.org/api/views/metadata/v1/{dataset_id}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

#    # Example: Get metadata for the Crime dataset (ID: ijzp-q8t2)
#    metadata = get_dataset_metadata("ijzp-q8t2")
#    print(metadata)

def list_columns(dataset_id):
    """Get column names for a given dataset."""
    metadata = get_dataset_metadata(dataset_id)

    columns = metadata.get("columns", [])
    for col in columns:
        print(f"{col['name']} (Type: {col['dataTypeName']})")

#    # Example: Check columns in the Crime dataset
#    list_columns("ijzp-q8t2")
class ChicagoDataAPI:
    BASE_URL = "https://data.cityofchicago.org/resource"

    def __init__(self, dataset_id=None, app_token=None):
        """
        Initialize the API wrapper.

        :param dataset_id: The ID of the dataset (e.g., 'ijzp-q8t2' for crime data).
        :param app_token: Optional Socrata app token (recommended for high-rate usage).
        """
        self.dataset_id = dataset_id
        self.app_token = app_token

    def get_data(self, limit=10, filters=None, order_by=None):
        """
        Fetch data from the dataset.

        :param limit: Number of records to retrieve.
        :param filters: Dictionary of query filters (e.g., {"primary_type": "THEFT"}).
        :param order_by: Column name to sort results by.
        :return: List of records (JSON format).
        """
        url = f"{self.BASE_URL}/{self.dataset_id}.json"
        params = {"$limit": limit}

        if filters:
            params.update(filters)

        if order_by:
            params["$order"] = order_by

        headers = {}
        if self.app_token:
            headers["X-App-Token"] = self.app_token

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise error for bad requests
        return response.json()


class MyTestCase(unittest.TestCase):
    crime_api = ChicagoDataAPI("ijzp-q8t2")  # Crime dataset
    data = crime_api.get_data(limit=5, filters={"primary_type": "THEFT"}, order_by="date")
    print(data)

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here
    def test_url_location(self):
        pass

    def test_url_variables(self):
        pass

    def test_set_url(self):
        pass
    def test_get_population(self):
        pass
# Example usage
if __name__ == "__main__":
    unittest.main()
