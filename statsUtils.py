import numpy as np
from scipy import stats

def create_ratio_column(df, column_numerator, column_denominator, new_column_name):
    df[new_column_name] = df[column_numerator] / df[column_denominator]

def get_quantile_values(df, column_name, quantiles):
    #q = z_df['Z-SUM'].quantile([0.00, 0.333, 0.667, 1.00])
    return df[column_name].quantile(quantiles)

def sum_zscores_accross_columns(df, z_score_columns):
    #columns = df.columns.drop('NAME')
    #columns = columns.drop('Population')
    df['Z-SUM'] = df[z_score_columns].sum(axis=1)
    return df

def restrict_dataset_by_max_column_variable(df, column_variable, limit):
    #df = df[(df['Population'] < 250000)]
    df = df[(df[column_variable] < limit)]
    return df

def restrict_dataset_by_min_column_variable(df, column_variable, limit):
    #df = df[(df['Population'] < 250000)]
    df = df[(df[column_variable] > limit)]
    return df

def remove_outliers_from_column_by_std_dev(df, column_variable, std_dev=3):
    return df[(np.abs(stats.zscore(df[column_variable])) < std_dev)]
    #df[['NAME', 'Population']].sort_values('Population')

def get_boxplt(df, column_array):
    boxplot = df.boxplot(column=column_array)
    return boxplot

def apply_zscores(df, zscore_columns):
    z_df = df
    #columns = z_df.columns.drop('NAME')
    #columns = columns.drop('Population')
    z_df[zscore_columns].apply(stats.zscore)
    return z_df

def set_table_data_types(df, columns, type):  #input dict with label -> data_type mappings?
    for var_name in columns:
        set_column_data_type(df, var_name, type)
def set_column_data_type(df, var_name, type):
    df[var_name] = df[var_name].astype(type)
