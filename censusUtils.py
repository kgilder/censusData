import os
import unittest
import re
import zipfile

import pandas as pd
from census import Census
import us  # Helps convert state names to abbreviations
from dotenv import load_dotenv
import geopandas as gpd
import requests

def dataset_html_to_str(html_str):
    dataset_str = html_str.replace('› ', '/')
    return dataset_str

def dataset_str_to_html(dataset_str):
    html_str = dataset_str.replace('/', '› ')
    return html_str

def get_census_dict():
    census_data_url = "https://api.census.gov/data.html"
    census_table = pd.read_html(census_data_url)
    census_table = census_table[0][:-1]
    census_dict = census_table.to_dict(orient='index')
    return census_dict

def get_list_url(api_base_url, list_name):
    return f"{api_base_url}/{list_name}.html"

def get_census_dict_by_dataset():
    census_data_url = "https://api.census.gov/data.html"
    census_table = pd.read_html(census_data_url)
    new_columns = {"Title": "title",
                   "Description": "description",
                   "Vintage": "year",
                   "Dataset Name": "dataset",
                   "Dataset Type": "type",
                   "Geography List": "geographies_url",
                   "Variable List": "variables_url",
                   "Group List": "groups_url",
                   "Examples": "examples_url",
                   "Developer Documentation": "documentation",
                   "API Base URL": "api_base_url"}
    updated_table = census_table[0].rename(columns=new_columns)
    headers = list(updated_table.columns.values)
    census_dict = updated_table[:-1].to_dict(orient='index')
    new_dict = {}
    for entry in census_dict:
        dataset = dataset_html_to_str(census_dict[entry]['dataset'])
        year = census_dict[entry]['year']
        if dataset not in new_dict:
            new_dict[dataset] = {}
        if year not in new_dict[dataset]:
            new_dict[dataset][year] = {}
        for label in headers:
            if re.search('url', label):
                new_dict[dataset][year][label] = get_list_url(census_dict[entry]['api_base_url'], census_dict[entry][label])
            else:
                new_dict[dataset][year][label] = census_dict[entry][label]
    return new_dict

def get_dataset_variables(variables_table_url):
    variables_table = pd.read_html(variables_table_url)
    variables_dict = variables_table[0].to_dict(orient='index')
    return variables_dict
def search_variables_by_field(dict, field_name, reg_ex):
    search_dict = {}
    for entry in dict.keys():
        if re.search(reg_ex, str(dict[entry][field_name]), re.IGNORECASE):
            search_dict[entry] = dict[entry]
    return search_dict

def get_variable_totals(dict):
    search_dict = {}
    for entry in dict.keys():
        if re.match('Estimate!!Total$', dict[entry]['Label']):
            search_dict[entry] = dict[entry]
    return search_dict
def search_variables_by_code(dict, name):
    return search_variables_by_name(dict, name)
def search_variables_by_name(dict, name):
    return search_variables_by_field(dict, 'Name', name)

def search_variables_by_label(dict, label_reg_ex):
    return search_variables_by_field(dict, 'Label', label_reg_ex)

def search_variables_by_concept(dict, concept_reg_ex):
    return search_variables_by_field(dict, 'Concept', concept_reg_ex)
def print_dict_entry(entry):
    print(f"{entry['Name']}:\t\t{entry['Concept']}\n")

def get_census_key_from_env(use_test_key=False):
    if os.path.exists('.env'):
        load_dotenv('.env')
        if use_test_key:
            census_key = os.getenv('TEST_KEY')
        else:
            census_key = os.getenv('CENSUS_KEY')
        return census_key
    else:
        print(f"WARNING: Can't load file {self.env_file_path}")
        return None

def get_state_geoid(state_name):
    """Get GEOID for a U.S. state."""
    c = Census(get_census_key_from_env())
    state_abbr = us.states.lookup(state_name).abbr
    data = c.sf1.get(("NAME", "STATE"), {"for": "state:*"})
    for entry in data:
        if entry["NAME"] == state_name:
            return entry["STATE"]
    return None
def get_geographies(address=None, geography_type=None):
    """
    Fetches geographical information for a given address, city, or state using the U.S. Census Geocoder API.
    :param address: One line address, can be a full address or a single state or zip code.
    :return: JSON with geographical information or an error message
    """

    base_url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
    params = {
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "layers": "10",  # FIPS codes and geography layers
        "format": "json",
        "address": address
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Check if results are available
        try:
            result = data['result']['addressMatches'][0]  # Get first match
            return {
                "matched_address": result.get("matchedAddress"),
                "coordinates": result.get("coordinates"),
                "geographies": result.get("geographies")
            }
        except (KeyError, IndexError):
            return {"error": "No matching address found. Try refining your input."}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}

def print_entire_dict_or_table(dict):
    for entry in dict:
        print_dict_entry(dict[entry])
def string_to_url(string):
    url_string = string.replace(" ", "%20")
    return url_string

class MyTestCase(unittest.TestCase):

    def test_something(self):
        census_dict = get_census_dict_by_dataset()
        self.assertEqual(True, True)  # add assertion here

    def test_varaibles_url(self):
        census_dict = get_census_dict_by_dataset()
        self.assertEqual('http://api.census.gov/data/2005/acs/acs1/variables.html', census_dict['acs/acs1']['2005']['variables_url'])

def download_and_extract_tiger(url, save_path, extract_to):
    """Downloads and extracts a TIGER/Line shapefile from the Census Bureau."""
    if not os.path.exists(save_path):
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print("Download complete.")
        else:
            raise Exception(f"Failed to download: {response.status_code}")

    # Extract the ZIP file
    print("Extracting files...")
    with zipfile.ZipFile(save_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

if __name__ == '__main__':
    unittest.main()
