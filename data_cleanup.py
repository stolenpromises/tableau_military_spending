"""Code written while learning beginner level pandas.

Short term objective: perform cleanup on input data for tableau.
Long term objective: learn pandas.

Created on Sun Dec 12 12:35:11 2021

@author: nathan.m
"""
import pandas as pd
import os
print(os.getcwd())

# =============================================================================
# read the datasets into dataframes
# =============================================================================
# read in a single csv
countries_selection = pd.read_csv(r'countries_selection.csv')
# the header row is missing...
# create a header row
selectionlist = ['country']  # list to append to
for year in range(1988, 2021):  # years to append
    selectionlist.append(year)
# now we have a header row to call
# perhaps we can append a header?
selection_header = pd.DataFrame(selectionlist)  # instantiate the header
c_selection = pd.DataFrame(pd.read_csv(r'countries_selection.csv'),
                           columns=selectionlist)
# above line resulted in NaN empty values
# passing the header row in as a 'names' parameter looks like the way to go
countries_selection = pd.read_csv(r'countries_selection.csv',
                                  names=selectionlist)
# now we have a dataframe with a proper header
countries = countries_selection['country']  # extract the select countries
# =============================================================================
# filter population and account balance data to include only the selection
countries_populations = pd.read_excel(r'countries_population.xls')
# attempting to filter by country
c_populations_selection = countries_populations.loc[countries['country'] is in countries_populations['Country Name'],]
# we seem to have a syntax error... let's poke around
countries_populations.xs['South Africa']
# 'method' object is not subscriptable
countries_populations.dtypes
# the country column of the dataset are all type() = object
# conversion to str() required
# indexing
countries_populations.loc[:, 'Country Name']
countries_populations.loc[0, 'Country Name']
countries.loc[0, 'country']
# filter series is the correct type for matching
type(countries[0])
# string conversion of objects at a particular index
test = str(countries_populations.loc[0, 'Country Name'])
type(test) # conversion working
# perhaps a for loop over country name?
for index in range(len(countries_populations)):
    # type conversion at index
    name = str(countries_populations.loc[index, 'Country Name'])
    # set at index
    countries_populations.at[index] = name
# did it work?
type(countries_populations.loc[0, 'Country Name'])
# win, perhaps now we can filter by the countries series


# =============================================================================
countries_account_balance = pd.read_excel(r'countries_account_balance.xls')