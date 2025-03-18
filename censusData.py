import unittest
from enum import Enum
from dotenv import load_dotenv
import os
import numpy as np
from censusUtils import string_to_url
from censusUtils import get_geographies
from censusUtils import get_census_key_from_env
import requests
import json
import pandas as pd
from census import Census

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
    geography = ''
    url_geography = ''
    geography_in = ''
    url_geography_in = ''
    census_key = ''
    env_file_path = '.env'
    dict = {}
    census_api_url = ''
    dataset = ''
    json = {}
    df = pd.DataFrame()

    def __init__(self, year='', dataset='', variables=[], geography='', geography_in='', use_test_key=False):
        self.census_api_base = 'https://api.census.gov'
        self.year = year
        self.dataset = dataset
        self.set_variables(variables)
        if geography:
            self.set_geography(geography)
        if geography_in:
            self.set_geography_in(geography_in)
        self.set_census_key(use_test_key=use_test_key)

    def print_info(self):
        print(f"census_api_base: {self.census_api_base}")
        print(f"year: {self.year}")
        print(f"dataset: {self.dataset}")
        print(f"variables: {self.variables}")
        print(f"url_variables: {self.url_variables}")
        print(f"geography: {self.geography}")
        print(f"url_geography: {self.url_geography}")
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

    def set_geography(self, geography, id=None):
        self.geography = geography
        if id:
            self.url_geography = "&for=" + string_to_url(geography) + ":" + id
        else:
            self.url_geography = "&for=" + string_to_url(geography) + ":*"

    def set_geography_in(self, geography, id = None):
        self.geography_in = expression
        if id:
            self.url_geography_in = "&in=" + geography + ":" + id
        else:
            self.url_geography_in = "&in=" + geography + ":*"

    def set_census_key(self, use_test_key=False):
        key = get_census_key_from_env(use_test_key=use_test_key)
        if not key:
            print("WARNING: No census api key provided.")
        else:
            self.census_key = key
    def get_url_geography(self):
        return self.url_geography
    def get_url_geography_re(self):
        return self.url_geography_in
    def get_url_variables(self):
        return self.url_variables

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset
    def set_census_api_url(self):
        self.census_api_url = f"{self.census_api_base}/data/{self.year}/{self.dataset}?get={self.url_variables}{self.url_geography}{self.url_geography_in}&key={self.census_key}"
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
    geography = censusLoc.MSA.value
    load_dotenv(dotenv_path='.env')
    census_key = get_census_key_from_env()

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_get_census_key(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=self.geography, use_test_key=True)
        self.assertEqual(acs_2005.get_census_key(), 'acedcafeacedcafe')

    def test_url_geography(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=self.geography)
        self.assertEqual(acs_2005.get_url_geography(), "&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*")

    def test_url_city_geography(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=censusLoc.CITY.value)
        self.assertEqual(acs_2005.get_url_geography(),"&for=principal%20city%20(or%20part):*")

    def test_url_variables(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=self.geography)
        self.assertEqual(acs_2005.get_url_variables(), "NAME,B01001_001E")

    def test_set_url(self):
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=self.geography)
        acs_2005.set_census_api_url()
        url_variables = acs_2005.get_url_variables()
        url_geography = acs_2005.get_url_geography()
        census_api = acs_2005.get_census_api_base()
        self.assertEqual(acs_2005.get_census_api_url(), f"{census_api}/data/{self.year}/{self.dataset}?get={url_variables}{url_geography}&key={self.census_key}")

    def test_get_us_population(self):
        us_geography = censusLoc.US.value
        acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=us_geography)
        acs_2005.collect_dataframe()
        pop_dict = acs_2005.get_dataframe().to_dict(orient='index')
        self.assertEqual('United States', pop_dict[0]['NAME'])
        self.assertEqual('288378137', pop_dict[0]['B01001_001E'])

    # def test_get_cities_population(self):
    #     city_geography = censusLoc.CITY.value
    #     illinois_geos = get_geographies(state="Illinois")
    #     acs_2005 = censusData(year=self.year, dataset=self.dataset, variables=self.variables, geography=city_geography)
    #     acs_2005.collect_dataframe()
    #     pop_dict = acs_2005.get_dataframe().to_dict(orient='index')
    #     print(pop_dict[0]['NAME'])
    #     #self.assertEqual('United States', pop_dict[0]['NAME'])
    #     #self.assertEqual('288378137', pop_dict[0]['B01001_001E'])

if __name__ == '__main__':
    unittest.main()
