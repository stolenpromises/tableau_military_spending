# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 12:35:11 2021

@author: nathan.m
"""
import os
print(os.getcwd())
import pandas as pd
countries_selection = pd.read_csv(r'countries_selection.csv')
countries_populations = pd.read_xls(r'countries_population.xls')
countries_account_balance = pd.read_xls(r'countries_account_balance.xls')
