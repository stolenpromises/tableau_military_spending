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

    def __init__(self, country_csv, datasets, columns_unwanted=[],
                 column_renames=[]):
        """Instatiates an CountryData object instance.

        Stores a pandas DataFrame of countries as imported from a csv file.

        Parameters
        ----------
        countries : STR
            String of csv filename containing countries.
        datasets: LIST of STR
            List of csv or xls filenames containing data for processing
        Returns
        -------
        None.

        """
        def add_column_labels(country_csv):
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
            rawdata_labelled = pd.read_csv(country_csv, names=selectionlist)
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
            alias_df = pd.DataFrame({'aliases': ['']})
            join_df = c_select.join(alias_df)  # append countries with aliases
            return join_df

        def dataset_clean(countries, df, columns_unwanted, column_renames):
            """Return a processed dataframe based on a selection of countries.

            Parameters
            ----------
            countries : DATAFRAME
                Two column DataFrame of countries and aliases
                    example:
                        columns | 'country', 'aliases'
                        rows | 'UAE', ['United Arab Emirates']
            df : DATAFRAME
                Many column DataFrame of countries and data by year
                    example:
                        columns | 'country', '1988', '1989'
                        rows | 'USA', 2000, 2200
                             | 'UAE', 1000, 1200
            columns_unwanted : LIST of STR
                List of strings identifying unwanted columns
            column_renames : DICT
                Dictionary of column names to rename
                    example:
                        {'old_col1':'new_col1', 'old_col2':'new_col2'}

            Returns
            -------
            df_clean : DATAFRAME
                Many column DataFrame containing relevant data for only select
                countries
            """
            # TODO testing DataFrame input
            countries = pd.DataFrame(drawnDataFrame)

            countries_populations = pd.read_excel(r'countries_population.xls')
            df = pd.DataFrame(countries_populations)
            # TODO end testing DataFrame input

            df_clean = pd.DataFrame(df)  # output DataFrame to mute
            # TODO possibly delete this?
            # df_select = df_clean[df_clean["country"].isin(countries)]

            # clean input DataFrame of unwanted columns
            for column in df:  # iterate over column lables
                # check for unwanted columns
                if column in columns_unwanted:
                    del df_clean[str(column)]  # delete it

            # rename columns based on column_renames
            df_clean = df_clean.rename(columns = column_renames)
            
            # filter based on country matches
            df_clean_cmatch = df_clean[df_clean["country"].isin(countries["country"])]
            
            # filter based on alias matches
            aliaslist = []  # superset to append to
            for value in countries["aliases"]:  # iterate: aliases series
                if type(value) is list:  # aliases are present
                    for item in value:  # iterate over the aliases
                        aliaslist.append(item)  # append the alias
            df_clean_amatch = df_clean[df_clean["country"].isin(aliaslist)]
            df_concat = pd.concat([df_clean_cmatch, df_clean_amatch])
            # append the two together
            # revised iteration over DataFrame rows
            # iterate over select countries and aliases as a series
            for label, series in countries.items():  # pull each series
                for index, c_clean in df_clean['country'].items():
                    print('c_clean is: ', c_clean)
                # iterate over all countries and aliases
                if c_clean in series:
                    test = 'match'
                    break
                else:
                    print('no match')
                print('label is: ', label)
                print('series is: ', series)

                #for index, value in countries["country"].items():
                    #if country in value 
# =============================================================================
#             # iterate over each DataFrame index row
#             for country in df["Country Name"]:  # iterate over rows
#                 match = False  # match trigger
#                 # iterate over select country primary names
#                 for select_country in countries["country"]:
#                     if country == select_country:  # primary name match
#                         match = True
#                 # iterate over select country aliases
#                 for select_aliases in countries["country"]:  # alias list
#                     for alias in select_aliases:  # alias
#                         if alias == select_country:  # alias match
#                             match = True
#                 if match is True:  # match was found
#                     # append the data
#                     # set 
#             return df_clean
# =============================================================================
        self.columns_unwanted = columns_unwanted
        self.column_renames = column_renames
        # store dataframe csv import
        self.countries_raw = pd.read_csv(country_csv)
        # establish countries and years
        # header row creation, if required
        if self.countries_raw.columns[0] != 'country':  # country NOT found
            # send for labelling
            self.countries_selection = add_column_labels(country_csv)
        else:  # country found
            self.countries_selection = self.countries_raw
        # establish baseline country list and aliases
        self.countries = country_build(self.countries_selection)
        self.datasets = datasets  # list of dataset filenames
        self.df_raw = []  # list of raw dataframes before processing
        self.df_processed = []  # list of processed dataframes
            
    def get_data(self, datasets=[]):  # TODO dataset specification
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
        countries = self.countries  # abstraction for code simplification
        if country in countries['country'].values:
            # a match has been found - append the alias
            # abstract out the target country
            target_c = countries.loc[countries['country'] == country]
            target_index = target_c.index.tolist()[0]  # country index
            existing_aliases = countries.at[target_index, 'aliases']
            if type(existing_aliases) is list:  # aliases exist
                countries.at[target_index, 'aliases'].append(alias)  # append
            else:  # no aliases yet
                countries.at[target_index, 'aliases'] = [alias]  # set a list
        else:  # country not found in DataFrame
            print('Country not found in CountryData.countries')
            return()

        # print confirmation and the outcome
        print()
        print('country DataFrame updated')
        print(self.countries.loc[countries['country'] == country])
        print()
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
        # check for the country within CountryData.countries DataFrame
        countries = self.countries  # abstraction for code simplification
        if country in countries['country'].values:
            # a match has been found - get the alias
            # abstract out the target country
            target_c = countries.loc[countries['country'] == country]
            target_index = target_c.index.tolist()[0]  # country index
            existing_aliases = countries.at[target_index, 'aliases']
            if type(existing_aliases) is float:  # no aliases exist
                print()
                print('No aliases for', country)
                print()
                return()
            else:  # aliases exist
                print()
                print(country, ' aliases are:', existing_aliases)
                print()
                return()
        else:  # country not found in DataFrame
            print()
            print('Country not found in CountryData.countries')
            print()
            return()


# unwanted columns that will be culled from all datasets
columns_unwanted = ['Country Code']

# column renames that will be applied to all datasets
column_renames = {'Country Name': 'country'}

# input datasets
datasets = ['countries_selection.csv', 'countries_populations.xls',
            'countries_account_balance.xls']

# object instantiation
clist = CountryData('countries_selection.csv', datasets, columns_unwanted,
                    column_renames)

# use the get_data method to draw out a DataFrame
drawnDataFrame = clist.get_data()
print(drawnDataFrame)  # print the dataframe

# set_aliases for missing countries from the selection
clist.set_alias('UAE', 'United Arab Emirates')
clist.set_alias('Egypt', 'Egypt, Arab Rep.')
clist.set_alias('Korea, North', "Korea, Dem. People's Rep")
clist.set_alias('Korea, South', "Korea, Rep.")
clist.set_alias('Russia', "Russian Federation")
clist.set_alias('USA', "United States")
clist.set_alias('Viet Nam', "Vietnam")
drawnDataFrame = clist.get_data()  # use the get_data method to return updated DataFrame

# get_alias method test
clist.get_alias('UAE')
clist.get_alias('Taiwan')

# output population DataFrame


# =============================================================================
# TODO methods
#        def add_country(self, country, aliases:
#             """ Append a country to AliasLookup."""
#         def clr_country:
#         def get_countries:
# =============================================================================

