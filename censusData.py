import unittest
from enum import Enum
from dotenv import load_dotenv
import os
import numpy as np
from censusUtils import string_to_url
import requests
import json
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
    url_variables = ''
    location = ''
    url_location = ''
    census_key = ''
    env_file_path = '.env'
    dict = {}
    census_api_url = ''
    dataset = ''
    json = {}
    df = pd.DataFrame()

    def __init__(self, year='', dataset='', variables=[], location='', census_key=''):
        self.census_api_base = 'https://api.census.gov'
        self.year = year
        self.dataset = dataset
        self.set_variables(variables)
        self.set_location(location)
        self.set_census_key(census_key)

    def print_info(self):
        print(f"census_api_base: {self.census_api_base}")
        print(f"year: {self.year}")
        print(f"dataset: {self.dataset}")
        print(f"variables: {self.variables}")
        print(f"url_variables: {self.url_variables}")
        print(f"location: {self.location}")
        print(f"url_location: {self.url_location}")
        print(f"env_file_path: {self.env_file_path}")

    def get_census_api_base(self):
        return self.census_api_base

    def set_env_file_path(self, env_file_path):
        self.env_file_path = env_file_path
    def get_census_key(self):
        return self.census_key
    def set_variables(self, variables):
        self.variables = variables
        self.url_variables  = ','.join(['NAME'] + variables)

    def set_location(self, location):
        self.location = location
        self.url_location = string_to_url(location)
    def set_census_key_from_env(self, use_test_key=False):
        if os.path.exists(self.env_file_path):
            load_dotenv(self.env_file_path)
            if use_test_key:
                self.census_key = os.getenv('TEST_KEY')
            else:
                self.census_key = os.getenv('CENSUS_KEY')
            return True
        else:
            print(f"WARNING: Can't load file {self.env_file_path}")
            return False

    def set_census_key(self, census_key):
        if census_key != '':
            self.census_key = census_key
        else:
            if not self.set_census_key_from_env():
                print("WARNING: No census api key provided.")
    def get_url_location(self):
        return self.url_location
    def get_url_variables(self):
        return self.url_variables

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset
    def set_census_api_url(self):
        self.census_api_url = f"{self.census_api_base}/data/{self.year}/{self.dataset}?get={self.url_variables}&for={self.url_location}&key={self.census_key}"
    def get_census_api_url(self):
        return self.census_api_url
    def get_variable_dataframe(self):
        return 0

    def get_api_url_response(self):
        response = requests.get(self.census_api_url)
        self.json = json.loads(response.text)

    def collect_dataframe(self):
        self.dict = {}
        self.set_census_api_url()
        self.get_api_url_response()
        header = self.json[0][:-1]
        for label in header:
            self.dict[label] = []
        for row in self.json[1:]:
            for i in range(len(row[:-1])):
                self.dict[header[i]].append(row[i])
        self.df = pd.DataFrame(self.dict)

    def get_dataframe(self):
        return self.df

class MyTestCase(unittest.TestCase):
    variables = ['B01001_001E']
    year = '2005'
    dataset = 'acs/acs1'
    location = censusLoc.MSA.value
    load_dotenv(dotenv_path='.env')
    census_key = os.environ.get('CENSUS_KEY')

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_get_census_key(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, location=self.location, census_key='12345678')
        self.assertEqual(acs_2005.get_census_key(), '12345678')
        acs_2005.set_census_key_from_env(use_test_key=True)
        self.assertEqual(acs_2005.get_census_key(), 'acedcafeacedcafe')

    def test_url_location(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, location=self.location, census_key=self.census_key)
        self.assertEqual(acs_2005.get_url_location(), "metropolitan%20statistical%20area/micropolitan%20statistical%20area")

    def test_url_variables(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, location=self.location, census_key=self.census_key)
        self.assertEqual(acs_2005.get_url_variables(), "NAME,B01001_001E")

    def test_set_url(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, location=self.location, census_key=self.census_key)
        acs_2005.set_census_api_url()
        url_variables = acs_2005.get_url_variables()
        url_location = acs_2005.get_url_location()
        census_api = acs_2005.get_census_api_base()
        self.assertEqual(acs_2005.get_census_api_url(), f"{census_api}/data/{self.year}/{self.dataset}?get={url_variables}&for={url_location}&key={self.census_key}")

    def test_get_us_population(self):
        us_location = censusLoc.US.value
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, location=us_location, census_key=self.census_key)
        acs_2005.collect_dataframe()
        pop_dict = acs_2005.get_dataframe().to_dict(orient='index')
        self.assertEqual('United States', pop_dict[0]['NAME'])
        self.assertEqual('288378137', pop_dict[0]['B01001_001E'])

if __name__ == '__main__':
    unittest.main()
