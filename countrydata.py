"""Code written while learning beginner level pandas.

In completing data_cleanup.py, I'm realizing I will probably need further
abstraction.

Created on Sat Dec 18 13:14:19 2021

@author: nathan.m
"""
import pandas as pd
import numpy as np
import os
# TODO remove sys, not needed
import sys
#

# TODO update parameter defintions
class CountryData(object):
    """Collection of country names, aliases and associated data."""

    def __init__(self, country_csv, datasets, aliases, columns_unwanted=[],
                 column_renames=[], country_clrs=[]):
        """Instatiates an CountryData object instance.

        Stores a pandas DataFrame of countries as imported from a csv file.

        Parameters
        ----------
        countries : STR
            String of csv filename containing countries.
        datasets: LIST of STR
            List of csv or xls filenames containing data for processing
        aliases : List of TUP
            List of tuples in the format:
                ('country', 'country alias')
                ex:
                ('UAE', 'United Arab Emirates')

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
            emptylists = []  # empty list to append lists to
            for iteration in range(len(c_select)):  # iterate for each country
                emptylists.append([])
            alias_df = pd.DataFrame({'aliases': emptylists})
            join_df = c_select.join(alias_df)  # append countries with aliases
            return join_df

        def set_alias(country, alias):
            """Append an alias for a country.

            Given a country name found in CountryData.countries
            DataFrame['country'] appends a new alias for that country.

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
                    # append
                    countries.at[target_index, 'aliases'].append(alias)
                else:  # no aliases yet
                    # set a list
                    countries.at[target_index, 'aliases'] = [alias]
            else:  # country not found in DataFrame
                print('country is ', country)
                print('alias is ', alias)
                print('Country not found in CountryData.countries')
                return()

            # print confirmation and the outcome
            # print()
            # print('countries DataFrame updated')
            # print(self.countries.loc[countries['country'] == country])
            # print()
            return()

        def set_country(self, c_from, c_to):
            """Change an existing country entry.

            Parameters
            ----------
            c_from : STR
                Country to change.
            c_to : STR
                Name to change the country to.

            Returns
            -------
            aliaslist : LIST
                A list of aliases resolved from the parent CountryData object.

            """
            # check for the country within CountryData.countries DataFrame
            countries = self.countries  # abstraction for code simplification
            if c_from in countries['country'].values:
                # a match has been found
                # abstract out the target country
                target_c = countries.loc[countries['country'] == c_from]
                target_index = target_c.index.tolist()[0]  # country index
                countries.loc[[target_index], ['country']] = c_to  # mute entry
                self.countries = countries
                print()
                print(c_from, ' changed to:', countries.loc[[target_index],
                                                            ['country']])
                print()
                return()
            else:  # country not found in DataFrame
                print()
                print('Country not found in CountryData.countries')
                print()
                return()

        def clr_country(self, country):
            """Change an existing country entry.

            Parameters
            ----------
            country : STR
                Country to clear.

            Returns
            -------
            None

            """
            # check for the country within CountryData.countries DataFrame
            countries = self.countries  # abstraction for code simplification
            if country in countries['country'].values:
                # a match has been found
                # abstract out the target country
                countries = countries[countries['country'] != country]
                self.countries = countries
                # print()
                # print(country, ' removed from DataFrame')
                # print()
                return()
            else:  # country not found in DataFrame
                print()
                print('Country not found in CountryData.countries')
                print()
                return()

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
            df_clean = pd.DataFrame(df)  # output DataFrame to mute

            # clean input DataFrame of unwanted columns
            for column in df:  # iterate over column lables
                # check for unwanted columns
                if column in columns_unwanted:
                    del df_clean[str(column)]  # delete it

            # rename columns based on column_renames
            df_clean = df_clean.rename(columns=column_renames)

            # rename DataFrame 'country' values to conform with countries
            # instatiate target DataFrame for muting operation
            df_clean_aliased = pd.DataFrame(df_clean)
            # print(df_clean.head())
            # sys.exit()
            for tup in df_clean.iterrows():  # iterate over rows in DataFrame
                df_clean_index = tup[0]  # store clean index... the mute target
                df_clean_country = tup[1]['country']  # store target country
                # iterate over rows in country DataFrame
                for tup in countries.iterrows():
                    series = tup[1]  # store countries series
                    country_correct = series[0]  # store country
                    country_aliases = series[1]  # store aliases
                    if country_aliases != []:  # aliases are present
                        # iterate over each alias
                        for alias in country_aliases:
                            # check for match to alias
                            if df_clean_country == alias:
                                # mute df_clean_aliased
                                df_clean_aliased.loc[df_clean_index, 'country'
                                                     ] = country_correct
            # target dataFrame now conforms with countries
            df_clean = pd.DataFrame(df_clean_aliased)  # reassignment

            # remove rows not found in countries DataFrame 'country'
            df_clean_sliced = df_clean[df_clean["country"].isin(countries[
                                                                'country'])]

            # compute countries that may be missing from df_clean
            dropframe = countries.drop(countries[countries["country"].isin
                                                 (df_clean_sliced["country"])
                                                 ].index)
            print()
            print('Dataset processed')
            print('There were ', len(dropframe), 'country entries that may')
            print('have not been found in the dataset.')
            print('they were:')
            print()
            for country in dropframe['country']:
                print(country)

            # target dataFrame now has been cleaned
            df_clean = df_clean_sliced

            # return the cleaned DataFrame.
            return(df_clean)
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
        for alias_tup in aliases:  # iterate over alias tuples
            # call the set alias method on that tuple
            set_alias(alias_tup[0], alias_tup[1])
        print(country_clrs)

        for country in country_clrs:  # iterate over country clears
            print(country)
            # sys.exit()
            clr_country(self, country)  # clear the country

        self.datasets = datasets  # list of dataset filenames
        self.df_raw = []  # list of raw dataframes before processing
        self.df_processed = []  # list of processed dataframes

        # for loop storing and cleaning datasets
        for dataset in self.datasets:  # loop over datasets
            filetype = dataset[-3:]  # identify the filetype
            if filetype == 'xls':
                df = pd.read_excel(dataset)  # store the DataFrame
                self.df_raw.append(df)  # append in raw format
                # call the clean method and append
                self.df_processed.append(dataset_clean(self.countries,
                                                       df,
                                                       self.columns_unwanted,
                                                       self.column_renames))
            if filetype == 'csv':
                df = pd.read_csv(dataset)  # store the DataFrame
            # check for a missing header
                if df.columns[0] != 'country':  # country NOT found
                    df = add_column_labels(dataset)  # send for labelling
                self.df_raw.append(df)  # append in raw format
                # call the clean method and append
                self.df_processed.append(dataset_clean(self.countries,
                                                       df,
                                                       self.columns_unwanted,
                                                       self.column_renames))

    def get_data(self):
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
        datasets : TUPLE of DATAFRAME
            countries_selection, LIST of processed DataFrames
        """
        return(self.countries, self.df_processed)

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

    def add_country(self, country, aliases=[]):
        """Append a country and alliases to the countries DataFrame.

        Parameters
        ----------
        country : STR
            Country name.
        alias : LIST of STR
            Associated alliases.

        Returns
        -------
        print() statement confirming the addition.

        """
        # build a DataFrame to append from
        append_df = pd.DataFrame([[country, aliases]], columns=['country',
                                                                'aliases'])
        # append to countries
        self.countries = self.countries.append(append_df)

        # print confirmation and the outcome
        # print()
        # print('countries DataFrame updated')
        # print(self.countries.loc[self.countries['country'] == country])
        # print()
        return()


# unwanted columns that will be culled from all datasets
columns_unwanted = ['Country Code']

# column renames that will be applied to all datasets
column_renames = {'Country Name': 'country'}

# input datasets
datasets = ['countries_per-cap.csv', 'countries_population.xls',
            'countries_account_balance.xls']
# datasets = ['countries_population.xls',
#             'countries_account_balance.xls']

# set_aliases for missing countries from the selection
aliases = [('UAE', 'United Arab Emirates'),
           ('Egypt', 'Egypt, Arab Rep.'),
           ('Korea, North', "Korea, Dem. People's Rep"),
           ('Korea, South', "Korea, Rep."),
           ('Russia', "Russian Federation"),
           ('USA', "United States"),
           ('Viet Nam', "Vietnam"),
           ('Venezuela', "Venezuela, RB"),
           ('UK', "United Kingdom"),
           ('Syria', "Syrian Arab Republic"),
           ('Iran', "Iran, Islamic Rep."),
           ('Yemen', "Yemen, Rep.")]

# correct these country names - not yet needed, but the method is functional
# c_corrections = [('Germany DR]

# clear these unwanted countries
country_clrs = ['German DR']

# object instantiation
clist = CountryData('countries_selection.csv', datasets, aliases,
                    columns_unwanted, column_renames, country_clrs)

# set_alias() method test
# clist.set_alias('Iran', "Iran, Islamic Rep")

# get_alias method test
# clist.get_alias('UAE')
# clist.get_alias('Taiwan')

# add_country() method test
# clist.add_country('Serbia')  # a country with no aliases

# rename a country test
# clist.set_alias("German DR", 'Germany', )
# output population DataFrame

# use the get_data method to draw out processed DataFrames
drawnDataFrames = clist.get_data()
countries = drawnDataFrames[0]
per_cap_spending = drawnDataFrames[1][0]
populations = drawnDataFrames[1][1]
account_balance = drawnDataFrames[1][2]
