import unittest
from enum import Enum
import numpy as np
from censusData import *

class acs_api(Enum):
    URL = 'https://api.census.gov'
class acs_type(Enum):
    ACS1 = '1'
    ACS5 = '5'
class acs_location(Enum):
    US = 'us'
    STATE = 'state'
    COUNTY = 'county'
    MSA = 'metropolitan statistical area/micropolitan statistical area'
    CITY = 'principal city (or part)'
    CSA = 'combined statistical area'

class acs_variable_codes(Enum):
    POPULATION = 'B01001_001E'
    EMPLOYMENT = 'B23001_001E'
    EARNINGS   = 'B19051_001E'
    HOUSEHOLD_INCOME = 'B19001_001E'
    ANNUAL_WAGES = 'B19052_001E'
    POVERTY_RATIO = 'B17002_001E'

available_sets = {
    acs_type.ACS1: {
        'years': np.arange(2005,2022, 1),
    },
    acs_type.ACS5: {
        'years': np.arange(2009, 2022, 1)
    }
}

class acsVar():
    label = ''
    code = ''
    def __init__(self, label, code):
        self.label = label
        self.code = code

class acs1Data(censusData):
    def __init__(self, year='', variables=[], location='', census_key=''):
        super().__init__(year=year, dataset='acs/acs1', variables=variables, location=location, census_key=census_key)

class acs5Data(censusData):
    def __init__(self, year='', variables=[], location='', census_key=''):
        super().__init__(year=year, dataset='acs/acs5', variables=variables, location=location, census_key=census_key)


class MyTestCase(unittest.TestCase):
    variables = ['B01001_001E']
    year = '2005'
    location = censusLoc.MSA.value
    load_dotenv(dotenv_path='.env')
    census_key = os.environ.get('CENSUS_KEY')

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_url_location(self):
        acs_2005 = acs1Data(year=self.year, variables=self.variables, location=self.location, census_key=self.census_key)
        self.assertEqual(acs_2005.get_url_location(), "metropolitan%20statistical%20area/micropolitan%20statistical%20area")

    def test_url_variables(self):
        acs_2005 = acs1Data(year=self.year, variables=self.variables, location=self.location, census_key=self.census_key)
        self.assertEqual(acs_2005.get_url_variables(), "NAME,B01001_001E")

    def test_set_url(self):
        acs_2005 = acs1Data(year=self.year, variables=self.variables, location=self.location, census_key=self.census_key)
        acs_2005.set_census_api_url()
        url_variables = acs_2005.get_url_variables()
        url_location = acs_2005.get_url_location()
        census_api = acs_2005.get_census_api_base()
        self.assertEqual(acs_2005.get_census_api_url(), f"{census_api}/data/{self.year}/{acs_2005.get_dataset()}?get={url_variables}&for={url_location}&key={self.census_key}")

    def test_get_us_population(self):
        us_location = censusLoc.US.value
        acs_2005 = acs1Data(year=self.year, variables=self.variables, location=us_location, census_key=self.census_key)
        acs_2005.collect_dataframe()
        pop_dict = acs_2005.get_dataframe().to_dict(orient='index')
        self.assertEqual('United States', pop_dict[0]['NAME'])
        self.assertEqual('288378137', pop_dict[0]['B01001_001E'])

if __name__ == '__main__':
    unittest.main()
