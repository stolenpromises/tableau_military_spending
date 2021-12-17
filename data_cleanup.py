"""Code written while learning beginner level pandas.

Short term objective: perform cleanup on input data for tableau.
Long term objective: learn pandas.

Created on Sun Dec 12 12:35:11 2021

@author: nathan.m
"""
import pandas as pd
import os
print(os.getcwd())
## = troubleshooting lines of code. these lines should not be run.
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
# we seem to have a syntax error... let's poke around
# countries_populations.xs['South Africa']
# 'method' object is not subscriptable
countries_populations.dtypes
# the country column of the dataset are all type() = object
# conversion to str() required
# indexing
countries_populations.loc[:, 'Country Name']
countries_populations.loc[0, 'Country Name']
countries.loc[0]  # indexing on series does not include a column index
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
# filter based on a row query
s_cpop = countries_populations[countries_populations['Country Name'] == 'Canada']
# the filter is matching based on the string key
# the dataset was spoiled earlier though... troubleshoot
# =============================================================================
# database spoiled earlier... why? suspect object to str type conversion
# =============================================================================
c_pop = pd.read_excel(r'countries_population.xls')
for index in range(len(c_pop)):
    # type conversion at index
    name = str(c_pop.loc[index, 'Country Name'])
    # set at index
    c_pop.at[index, 'Country Name'] = name
test = str(c_pop.loc[0, 'Country Name'])
type(test) # conversion working
# was missing column index... solved
# =============================================================================
# =============================================================================
# the database is repaired... now try again at filtering based on country
# =============================================================================
s_c_pop = c_pop[c_pop['Country Name'] == 'Canada']
# alright... we've got a working filter based on a string index
# now we need to filter based on one of many keys
## s_c_pop = c_pop[c_pop['Country Name'] in countries]
# series is unhashable. appears related to dtype
countries = pd.Series(countries_selection['country'], dtype=str)
##s_c_pop = c_pop[c_pop['Country Name'] in countries]
## countries.loc[countries == 'Canada']
# above is sucessfully matching within the series based on a key
## troubleshooting
## s_c_pop = c_pop[c_pop['Country Name'] in countries.loc['Canada']
## True == countries.str.contains(countries['country'])
## 'Canada' in countries.values
## countries.loc['country'] == 'Canada'
## for country in countries.items():
##   print(country{value})
#testtuple = (91, 'Yemen')
print(countries.values)
# ahh.... values.... duh
##s_c_pop = c_pop[c_pop['Country Name'] in countries.values]
# above requires lengths to match... perhaps a for loop over each item
# do i need to set an initial datatype for the dataframe append target?
## d = {'country': [str()], 'floater': []}
## s_c_pop = pd.DataFrame(data = {['country':, dtype=str], ['floater': dtype=float]})
d = {'country': [], 'floater': []}
s_c_pop = pd.DataFrame(data=d)
# ok, we have created a dataframe with a header...
# perhaps a blank dataframe can be appended to...
s_c_pop = pd.DataFrame()
appended_df = s_c_pop.append({'country': 'argentina', 'floater': 3.445}, ignore_index=True)
# we can append a dataframe and it's our choice if we use lines to extract
for index in range(len(c_pop)):  # iterate over each item in c_pop
    if c_pop.loc[index, 'Country Name'] in countries.values:
        # country selection match - append to new dataframe
        
list1[]

countries_account_balance = pd.read_excel(r'countries_account_balance.xls')