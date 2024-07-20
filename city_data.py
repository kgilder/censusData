from censusUtils import get_acs_variable_data, get_census_dict_by_dataset

#
#  MAIN
#

population_var = 'B01001_001E' #Population
employment_var = 'B23001_001E' #employed?
earnings_var = 'B19051_001E'
median_earnings_var = 'B20004_001E'
household_income_var = 'B19001_001E'
wage_or_salary_var = 'B19052_001E'
poverty_ratio_var = 'B17002_001E'

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
variables = [population_var, employment_var, earnings_var, median_earnings_var, household_income_var, poverty_ratio_var]
msa_pop_2005 = get_acs_variable_data(year, variables)
