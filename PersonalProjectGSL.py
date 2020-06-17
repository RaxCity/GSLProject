# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 09:23:20 2020

Personal project to help me learn some python web scraping. Parsing Liquipedia's GSL results to find winners.

@author: akavcioglu
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from GSLTest import GSLWebpageParser
import GSLHelperFunctions as ghf
import os

df = pd.DataFrame()

def return_df():
    global df
    return df

def getPositiveNumberInput(prompt):
    number = -1
    while number <= 0:    
        number = int(input(prompt))
    return number

def getPlayerInput():
    prompt = input('Which player do you want information for?\n')
    player = str(prompt)
    return player

def load():
    URL = 'https://liquipedia.net/starcraft2/Global_StarCraft_II_League'
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    results = soup.find(id = 'mw-content-text')
    
    tables = results.find_all('table', class_ = 'wikitable collapsible')
    
    URLList = []
    RealURLList = []
    
    for table in tables:
        event_elems = table.find_all('tr')
        for event_elem in event_elems:
            for a in event_elem.find_all('a', href=True):
                URLList.append(a['href'])          
                
    for item in URLList:
        if('StarCraft_II_Open' in item) or ('Global_StarCraft_II_League' in item) or ('WCS' in item):
            RealURLList.append(item)
    
    #looking at this line gets you banned
    RealURLList.pop()
    return RealURLList

def create_csv():
    global df
    RealURLList = load()
    for link in RealURLList:
        print('Loading results for ' + str(link))
        df = df.append(GSLWebpageParser('https://liquipedia.net' + link))
    if os.path.isfile('gsl_data.csv'):
        os.remove('gsl_data.csv')
    df.to_csv('gsl_data.csv', index_label = 'index')

def read_csv():
    global df
    df = pd.read_csv('gsl_data.csv', index_col = 'index')
    ghf.createFrames(df)

def beginProcess():
    global df
    ghf.createFrames(df)
    print('\nWelcome to the GSL Database')
    print('Press a key to continue')
    option = 100
    while option != 8:
        option = 100
        print('\n1: Display top earners')
        print('2: Display most active GSL participants')
        print('3: Display results for a player')
        print('4: Display number of times a player competed')
        print('5: Find earnings for a player')
        print('6: Find a player\'s position on the earnings list')
        print('7: Compare two players')
        print('8: Quit')
        while option > 8:
            prompt = ''
            option = getPositiveNumberInput(prompt)
        if option == 1:
            prompt = 'How many earners should be displayed?\n'
            number = getPositiveNumberInput(prompt)
            tf = ghf.topEarners()
            print(tf.head(number))
        elif option == 2:
            prompt = 'How many participants should be displayed?\n'
            number = getPositiveNumberInput(prompt)
            tf = ghf.highestCounts()
            print(tf.head(number))
        elif option == 3:
            player = getPlayerInput()
            ghf.displayResults(player)
        elif option == 4:
            player = getPlayerInput()
            print(player + ' has competed ' + str(ghf.getCount(player)) + ' times in GSL.')
        elif option == 5:
            player = getPlayerInput()
            print(player + ' has earned $' + str(ghf.findPlayerWorth(player)) + ' in GSL')
        elif option == 6:
            player = getPlayerInput()
            print(player + ' is number ' + str(ghf.findEarningsPosition(player).index[0]) + ' on the GSL earnings list')
        elif option == 7:
            print('You will now be asked for the two players you wish to compare')
            player1 = getPlayerInput()
            player2 = getPlayerInput()
            print(ghf.compareTwoPlayers(player1, player2))
        elif option == 8:
            print('Goodbye')
        else:
            print('How did I get here??')
