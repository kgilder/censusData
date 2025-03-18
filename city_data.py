from censusUtils import *
from acsData import acs1Data
from censusData import *
from dotenv import load_dotenv
from plotnine import ggplot, aes, geom_point


population_var = 'B01001_001E' #Population
employment_var = 'B23001_001E' #employed?
earnings_var = 'B19051_001E'
median_earnings_var = 'B20004_001E'
household_income_var = 'B19001_001E'
wage_or_salary_var = 'B19052_001E'
poverty_ratio_var = 'B17002_001E' #Should be sum of 002E, 003E, 004E

label_dict = {
    population_var: 'Population',
    employment_var: 'Employment',
    earnings_var: 'Earnings',
    median_earnings_var: 'Median Earnings',
    household_income_var: 'Household Income',
    wage_or_salary_var: 'Wage/Salary',
    poverty_ratio_var: 'Poverty Ratio'
}

census_dict = get_census_dict_by_dataset()

year = '2005'
dataset = 'acs/acs1'
location = censusLoc.MSA.value
variables = [population_var, employment_var, earnings_var, median_earnings_var, household_income_var, poverty_ratio_var]

acs_2005 = acs1Data(year=year, variables=variables, location=censusLoc.MSA.value)
acs_2005.set_census_key_from_env()
acs_2005.collect_dataframe()
acs_2005_dict = acs_2005.get_dataframe().to_dict(orient='index')

df = acs_2005.get_dataframe()
ggplot(df) + aes(x=population_var, y=median_earnings_var) + geom_point()


