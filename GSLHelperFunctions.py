# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:53:20 2020

@author: akavcioglu
"""
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
global rf
global df
global cf

def createFrames(df2):
    #@var rf Players with their aggregate earnings, easy to query and sort
    global rf
    #@var df Total dataframe
    global df
    #@var cf Country data
    global cf
    df = df2
    rf = df.drop(columns=['Tournament', 'Place', 'Team']).groupby('Player', as_index = False).sum()
    cf = df.drop(columns=['Race', 'Player', 'Tournament', 'Place', 'Team']).groupby('Country', as_index = False).sum()

def findPlayerWorth(playerName):
    try:
        return rf[rf['Player'].str.lower() == playerName.lower()].iloc[0][1]
    except:
        return 'Player not found!'
    
def topEarners():
    tf = rf.sort_values(by='$USD', ascending=False)
    tf.index = np.arange(1, len(tf)+1)
    return tf

def findPlayerResults(playerName):
    try:
        global df
        return df[df['Player'].str.lower() == playerName.lower()]
    except:
        raise

def displayResults(playerName):
    try:
        pf = findPlayerResults(playerName)
        if pf.empty:
            raise
    except:
        print('Player not found!')
        return
    pf['Tournament'] = pf['Tournament'].replace('Global StarCraft II League ' , '', regex=True).replace(' Korea GSL', '', regex=True).replace(' StarCraft II Open', '', regex=True)
    pf['Results'] = pf['Place'] + ' at ' + pf['Tournament'] + ' for ' + pf['$USD'].astype(str)
    print(pf['Results'].to_string())
    return

def getCount(playerName):
    pf = df[df['Player'].str.lower() == playerName.lower()]
    return pf['Tournament'].count()

def highestCounts():
    return df['Player'].value_counts()

def findEarningsPosition(playerName):
    tf = topEarners()
    if tf[tf['Player'].str.lower() == playerName.lower()].empty:
        return 'Player not found!'
    return playerName + ' is number ' + str(tf[tf['Player'].str.lower() == playerName.lower()].index[0]) + ' on the GSL earnings list'
    
def highestPlacing(playerName):
    try:
        pf = findPlayerResults(playerName)
    except:
        raise
    if pf.empty:
        return 'Player not found!'
    highest = pf.sort_index()['Place'].iloc[0]
    mod_pf = pf[pf['Place'] == highest]
    if len(mod_pf) == 1:
        return 'Highest placing is ' + str(highest) + ' at ' + mod_pf['Tournament'].iloc[0]
    else:
        return 'Highest placing is ' + str(highest) + ' at ' + str(len(mod_pf)) + ' tournaments'
    
def earningsPerTournament(playerName):
    try:
        return (findPlayerWorth(playerName)/getCount(playerName))
    except:
        return playerName + ' hasn\'t competed in any tournaments!'
    
def createCompareSeries(playerName):
    winnings = findPlayerWorth(playerName)
    num_events = getCount(playerName)
    per_event = earningsPerTournament(playerName)
    highest = highestPlacing(playerName)
    earningsPosition = findEarningsPosition(playerName)
    s = pd.Series([winnings, num_events, per_event, highest, earningsPosition], index=['Player Worth', 'Number of Events', 'Per-event Earnings', 'Highest Placing', 'Earnings Position'], name=playerName)
    return s

def compareTwoPlayers(player1, player2):
    return pd.concat([createCompareSeries(player1), createCompareSeries(player2)], axis=1)

def topCountryEarnings():
    global cf
    return cf.sort_values(by='$USD', ascending=False)

def promptRace(playerName):
    temp 