import unittest
import re
import pandas as pd

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
            if re.match(label, 'url'):
                new_dict[dataset][year][label] = get_list_url(census_dict[entry]['api_base_url'], census_dict[entry][label])
            else:
                new_dict[dataset][year][label] = census_dict[entry][label]
    return new_dict

def get_dataset_variables(variables_table_url):
    variables_table = pd.read_html(variables_table_url)
    variables_dict = variables_table.to_dict(orient='index')
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
        if re.match('Estimate Total$', dict[entry]['Label']):
            search_dict[entry] = dict[entry]
    return search_dict

def search_variables_by_name(dict, name):
    return search_variables_by_field(dict, 'Name', name)

def search_variables_by_label(dict, label_reg_ex):
    return search_variables_by_field(dict, 'Label', label_reg_ex)

def search_variables_by_concept(dict, concept_reg_ex):
    return search_variables_by_field(dict, 'Concept', concept_reg_ex)
def print_dict_entry(entry):
    print(f"{entry['Name']}:\t\t{entry['Concept']}\n")

def print_entire_dict_or_table(dict):
    for entry in dict:
        print_dict_entry(dict[entry])
def string_to_url(string):
    url_string = string.replace(" ", "%20")
    return url_string

class MyTestCase(unittest.TestCase):

    def test_something(self):
        new_census_dict = get_census_dict_by_dataset()
        self.assertEqual(True, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()
