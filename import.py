"""Code written while learning beginner level pandas.

In completing data_cleanup.py, I'm realizing I will probably need further
abstraction.

Created on Sat Dec 18 13:14:19 2021

@author: nathan.m
"""
import pandas as pd
import numpy as np
import os
class CountryData(object):
    """Collection of country names, aliases and associated data."""
    def __init__(self, filename):
        """Instatiates an AliasLoopup object instance.

        Stores a pandas DataFrame of countries as imported from a csv file.

        Parameters
        ----------
        filename : STR
            Name of the csv file.

        Returns
        -------
        None.

        """
        def add_column_labels(filename):
            """Add column labels to a raw dataset.

            Header layout:
                country | 1988 | 1989 | ... 2020 |

            Parameters
            ----------
            filename : DATAFRAME
                Name of the csv file needing column labels.

            Returns
            -------
            rawdata_labelled : DATAFRAME
                DataFrame with column labels.
            """
            # create a column label list
            selectionlist = ['country']  # list to append to
            for year in range(1988, 2021):  # years to append
                selectionlist.append(year)
            # create a new dataframe with labels
            rawdata_labelled = pd.read_csv(filename, names=selectionlist)
            return rawdata_labelled

        def country_build(countries_selection):
            """Return a 2 column DataFrame of country and aliases.

            Parameters
            ----------
            countries_selection : DATAFRAME
                A dataframe with minimum 1st column: 'country'

            Returns
            -------
            join_df : DATAFRAME
                A dataframe with layout:
                    example:
                        columns | 'country', 'aliases'
                        rows | 'UAE', NUN
            """
            # draw out the country column
            c_select = pd.DataFrame(countries_selection['country'], dtype=str)
            # build an empty alias dataframe to append on
            alias_df = pd.DataFrame({'aliases': []})
            join_df = c_select.join(alias_df)  # append countries with aliases
            return join_df
        self.rawdata = pd.read_csv(filename)  # store dataframe csv import
        # establish countries and years
        # header row creation, if required
        if self.rawdata.columns[0] != 'country':  # country NOT column label
            # send for labelling
            self.countries_selection = add_column_labels(filename)
        else:
            self.countries_selection = self.rawdata
        # establish baseline country list and aliases
        self.countries = country_build(self.countries_selection)
        self.datasets = []
    def get_data(self, datasets = []): #TODO dataset specification
        """Return cleaned DataFrames from the parent CountryData class.

        Parameters
        ----------
        countries : DATAFRAME
            A dataframe with layout:
                example:
                          'country',  | 'aliases'
                          ------------ ----------
                    row0 | 'UAE',     | 'United Arab Emirates'
                    row1 | 'Spain',   |  NUN
        sets : LIST

        Returns
        -------
        datasets : LIST
            List of DATAFRAME objects, country specific data.
        """
        return(self.countries)
    def set_alias(self, country, alias):
        """Append an alias for a country.

        Given a country name found in CountryData.countries DataFrame'country'
        appends a new alias for that country.

        Parameters
        ----------
        country : STR
            Country name.
        alias : STR
            Alias to append.

        Returns
        -------
        print() statement of the target country row.

        """
        # check for the country within CountryData.countries DataFrame
        if country in self.countries['country'].values:
            # a match has been found - append the alias
            
            existing_aliases = self.countries.at['country': country]
            #if existing_aliases = 
        else:  # country not found in DataFrame
            print('Country not found in CountryData.countries')
            return()

    def get_alias(self, country):
        """Return a list of aliases for a given country.

        Parameters
        ----------
        country : STR
            Country name.

        Returns
        -------
        aliaslist : LIST
            A list of aliases resolved from the parent CountryData object.

        """


# test code to draw out a dataframe for testing
clist = CountryData('countries_selection.csv')  # instantiate the object
test = clist.get_data()  # use the get_data method to draw out a DataFrame
print(test)  # print the dataframe


# =============================================================================
# TODO methods
#        def add_country(self, country, aliases:
#             """ Append a country to AliasLookup."""
#         def clr_country:
#         def set_alias:
#         def get_countries:
# =============================================================================
