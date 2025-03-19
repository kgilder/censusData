import unittest
from enum import Enum
from dotenv import load_dotenv
from censusUtils import get_census_key_from_env
import requests
import pandas as pd

class censusApi(Enum):
    URL = 'https://api.census.gov'

class censusLoc(Enum):
    US = 'us'
    STATE = 'state'
    COUNTY = 'county'
    MSA = 'metropolitan statistical area/micropolitan statistical area'
    CITY = 'principal city (or part)'
    CSA = 'combined statistical area'

class censusVar():
    label = ''
    code = ''
    def __init__(self, label, code):
        self.label = label
        self.code = code

class censusData():
    census_api_base = 'https://api.census.gov'
    year = ''
    variables = []
    geography = ''
    higher_geography = ''
    census_key = ''
    env_file_path = '.env'
    dict = {}
    census_api_url = ''
    dataset = ''
    params = {}
    json = {}
    df = pd.DataFrame()

    def __init__(self, year='', dataset='', variables=[], geography='', higher_geography=''):
        self.census_api_base = 'https://api.census.gov'
        if year:
            self.set_year(year)
        if dataset:
            self.set_dataset(dataset)
        if variables:
            self.set_variables(variables)
        if geography:
            self.set_geography(geography)
        if higher_geography:
            self.set_higher_geography(higher_geography)
        self.set_census_key()


    def update_url(self):
        self.census_api_url = f"{self.census_api_base}/data/{self.year}/{self.dataset}"

    def set_year(self, year):
        self.year = year
        self.update_url()

    def set_dataset(self, datasets):
        self.dataset = datasets
        self.update_url()

    def get_url(self):
        if not self.census_api_base:
            print('Error: census_api_base not set')
        if not self.year:
            print('Error: year not set')
        if not self.dataset:
            print('Error: dataset not set')
        return self.census_api_url

    def get_params(self):
        return self.params
    def update_year(self, year):
        self.year = year

    def update_dataset(self, dataset):
        self.dataset = dataset

    def get_census_key(self):
        return self.census_key

    def update_variables(self):
        self.params['get'] = ",".join(self.variables)

    def set_variables(self, variables):
        self.variables = variables
        self.update_variables()

    def clear_variables(self):
        self.variables = []
        del self.params['get']

    def add_variable(self, variable):
        self.variables.append(variable)
        self.update_variables()

    def set_geography(self, geography):
            self.params['for'] = geography

    def clear_geography(self):
        del self.params['for']

    def set_higher_geography(self, geography):
            self.params['in'] = geography

    def clear_higher_geography(self):
        del self.params['in']

    def set_census_key(self):
        key = get_census_key_from_env(use_test_key=False)
        if not key:
            print("WARNING: No census api key provided.")
        else:
            self.params['key'] = key

    def clear_census_key(self):
        del self.params['key']

    def get_api_response(self, url, params):
        response = requests.get(url, params)
        if response.status_code == 200:
            self.json = response.json()
        else:
            print("ERROR: Received invalid response: " + str(response.status_code))

    def collect_dataframe(self):
        self.dict = {}
        self.get_api_response(self.get_url(), self.get_params())
        header = self.json[0]
        for label in header:
            self.dict[label] = []
        for row in self.json[1:]:
            for i in range(len(row)):
                self.dict[header[i]].append(row[i])
        self.df = pd.DataFrame(self.dict)

    def get_dataframe(self):
        return self.df

class MyTestCase(unittest.TestCase):

    def test_get_us_population(self):
        us_geography = censusLoc.US.value
        acs_2005 = censusData(year='2005',
                              dataset='acs/acs1',
                              variables=['NAME','B01001_001E'],
                              geography='us:1')
        acs_2005.collect_dataframe()
        pop_dict = acs_2005.get_dataframe().to_dict(orient='index')
        self.assertEqual('United States', pop_dict[0]['NAME'])
        self.assertEqual('288378137', pop_dict[0]['B01001_001E'])

    def test_get_cities_population(self):
        cd = censusData(year='2010',
                              dataset='dec/sf1',
                              variables=['NAME','P001001'],
                              geography='block:*',
                              higher_geography='state:17 county:031'
                              )
        cd.collect_dataframe()
        dict = cd.get_dataframe().to_dict(orient='index')
        self.assertEqual('Block 1000, Block Group 1, Census Tract 101, Cook County, Illinois', dict[0]['NAME'])
        self.assertEqual('128', dict[0]['P001001'])

if __name__ == '__main__':
    unittest.main()
