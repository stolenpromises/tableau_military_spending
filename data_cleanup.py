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
# =============================================================================
# next
# =============================================================================
countries_populations = pd.read_excel(r'countries_population.xls')
countries_account_balance = pd.read_excel(r'countries_account_balance.xls')
