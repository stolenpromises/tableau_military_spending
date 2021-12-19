"""Code written while learning beginner level pandas.

Short term objective: perform cleanup on input data for tableau.
Long term objective: learn pandas.

Created on Sun Dec 12 12:35:11 2021

@author: nathan.m
"""
import pandas as pd
import numpy as np
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
        s_c_pop = s_c_pop.append(c_pop.loc[index])
# sucess! we have created a new dataframe based on the key search
# =============================================================================
# now need to store country codes and resolve/investigate why our filtered
# dataframe has only 74 rows vs the 94 of the select country dataframe
# =============================================================================
# lets do a sort based on name, so that the country list and the s_c_pop
# dataframes are easier to analyze
countries_selection = countries_selection.sort_values(by="country")
# perhaps easier to do a boolean of what was NOT included
countries_missing = pd.DataFrame()
for index in range(len(c_pop)):  # iterate over each item
    if c_pop.loc[index, 'Country Name'] not in countries.values:
        # country selection match - append to new dataframe
        countries_missing = countries_missing.append(c_pop.loc[index])
# i think it makes sense to conform to the world bank's choice of country name
# so we need to mute the countries_selection list to conform to that
c_miss_conform = pd.DataFrame()
for index in [8, 67, 126, 193, 202, 251, 257, 259]:  # iterate over the misses
    c_miss_conform = c_miss_conform.append(c_pop.loc[index])#  append them
# so these are our misses. it seems to make sense to explore an alias solution
# =============================================================================
# we need an alias solution. also we need a master country_selection dataframe
# which contains only countries
# =============================================================================
# countries_selection needs to be stored as what it actually is...
# countries selection per-capita
c_s_percapita = pd.DataFrame(countries_selection)
# now lets create a new dataframe to include only countries
c_select = pd.DataFrame(countries_selection['country'], dtype=str)
# add a column for an alias list
alias_df = pd.DataFrame({'aliases': []})
# empty dataframe of lists created... can we join it?
join_df = c_select.join(alias_df)
# yes we can... can we add a string to an entry?
## join_df.at[19, 'aliases'] = np.array(['test'])
# interpreter is complaining of 'setting an array element with a sequence'...
# what type is the target element?
type(join_df.at[19, 'aliases'])  # hmm... it's a float64
join_df.at[19, 'aliases'] = np.array([64.6])  # setting with a float works
# so why is this array a float array, when I specificed dtype above?
alias_df = pd.DataFrame({'aliases': []}, dtype=str)  # specify the dtype?
join_df = c_select.join(alias_df)
type(join_df.at[19, 'aliases'])  # now a float... ?
print(join_df.at[19, 'aliases'])
emptylist = []
type(emptylist)
emptylist.append('teststr')
# wait a minute... we should be able to just append to an empty list
join_df.at[19, 'aliases'] = np.array([64.6])
alias_df = pd.DataFrame({'aliases': ['']})  # an empty list perhaps?
type(join_df.at[19, 'aliases'])
join_df.at[19, 'aliases'] = ['test']  # sucess... hmm
type(join_df.at[19, 'aliases'])  # so an empty list will work fine?
alias_df = pd.DataFrame({'aliases': []})
join_df = c_select.join(alias_df)
join_df.at[19, 'aliases'] = ['test']  # confirmed
# adding aliases to the existing list is going to require checking for nan
# =============================================================================
# We've got a working framework for a country and [aliases] dataframe
# Now we'll need to write some code for appending to it. I smell def incoming
# =============================================================================
# need some ways to attain index
countries = test  # variable assignment from import.py memory scope
countryname = 'Taiwan'  # test query
# attain an index based on a country query
## test.query('country == ', countryname)
# index_label = int(test.query('country == ', countryname).index.tolist()[0])
# query won't work because syntax required passing in a string as syntax
# i need to pass in a string itself...# check if a list is already present
##answer = countries.loc[:,'Taiwan']
# this won't work because it only returns a string
countries['country'] == 'Taiwan'  # this works to pull out a truth/false table
countries.loc[countries['country'] == 'Taiwan']
# now we are pulling out a series with the original index number...
indextarget = countries.loc[countries['country'] == 'Taiwan'].index.tolist()
# now we have pulled the original index as a list
indextarget = countries.loc[countries['country'] == 'Taiwan'].index.tolist()[0]
# now we have an int.. we can use this for our set_alias method




























