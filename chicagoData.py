
import requests
import unittest
import geopandas as gpd
import matplotlib.pyplot as plt

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
import requests
import pandas as pd


class chicagoData:
    BASE_URL = "https://data.cityofchicago.org/resource"

    def __init__(self, dataset_id, fields=None, filters=None, order_by=None, limit=1000, app_token=None):
        """
        Initialize the API wrapper for the Chicago Data Portal.

        :param dataset_id: (str) Dataset ID from the Chicago Data Portal (e.g., '23tx-4h6r' for ward population)
        :param fields: (list) Fields/columns to retrieve (default: None = all fields)
        :param filters: (dict) Filtering conditions {column_name: value}
        :param order_by: (str) Column to sort by
        :param limit: (int) Number of results to fetch (default: 1000)
        :param app_token: (str) Optional Socrata app token for higher request limits
        """
        self.dataset_id = dataset_id
        self.fields = fields
        self.filters = filters
        self.order_by = order_by
        self.limit = limit
        self.app_token = app_token

    def get_url(self):
        """Constructs the API URL."""
        return f"{self.BASE_URL}/{self.dataset_id}.json"

    def get_params(self):
        """Generates query parameters."""
        params = {}

        # Select specific fields
        if self.fields:
            params["$select"] = ", ".join(self.fields)

        # Apply filters
        if self.filters:
            for key, value in self.filters.items():
                params[key] = value

        # Sorting
        if self.order_by:
            params["$order"] = self.order_by

        # Limit number of results
        params["$limit"] = self.limit

        # Add App Token if provided
        if self.app_token:
            params["$$app_token"] = self.app_token

        return params

    def get_data(self):
        """Fetches data from the Chicago Data Portal API."""
        url = self.get_url()
        params = self.get_params()

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)  # Convert to DataFrame
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


class MyTestCase(unittest.TestCase):
    crime_api = ChicagoDataAPI("ijzp-q8t2")  # Crime dataset
    data = crime_api.get_data(limit=5, filters={"primary_type": "THEFT"}, order_by="date")
    print(data)

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here
    def test_ward_population(self):
        # Ward Population Dataset ID from the portal
        dataset_id = "k5pk-wpt9"

        # Create API instance
        wards_api = chicagoData(
            dataset_id=dataset_id,
            fields=["acs_year", "ward", "total_population"],  # Select fields
            order_by="Ward",  # Order by ward number
            limit=50  # Fetch all wards
        )
        # Fetch data
        wards_df = wards_api.get_data()
        print(wards_df.head())
        # Load Chicago ward boundaries (GeoJSON format)
        wards_gdf = gpd.read_file("https://data.cityofchicago.org/resource/p293-wvbd.geojson")
        # Ensure ward numbers are stored as strings for merging
        wards_gdf["ward"] = wards_gdf["ward"].astype(str)
        # Print to verify structure
        print(wards_gdf.head())
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(12, 10))

        # Plot the merged GeoDataFrame
        merged_gdf.plot(column="total_population",
                        cmap="OrRd",  # Color scale (Red-Orange)
                        edgecolor="black",
                        linewidth=0.5,
                        legend=True,
                        legend_kwds={"shrink": 0.6, "label": "Population"},
                        ax=ax)

        # Add title
        ax.set_title("Population by Ward in Chicago", fontsize=14)

        # Remove axis for cleaner visualization
        plt.axis("off")

        # Show the map
        plt.show()

# Example usage
if __name__ == "__main__":
    unittest.main()
