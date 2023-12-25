# make sure color module is imported
import importlib.util
import sys

name = 'termcolor'

if name in sys.modules:
    print(f"{name!r} already in sys.modules")
elif (spec := importlib.util.find_spec(name)) is not None:
    # If you choose to perform the actual import ...
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
else:
    print(f"can't find the {name!r} module")
    exit()

import random, re, os
from termcolor import colored

def main():
    num_pattern = re.compile("^[0-9]+$")
    alpha_pattern = re.compile("^[A-Za-z]+$")
    global NUM_TURNS; NUM_TURNS = 100
    strat_1=0
    strat_2=0

    global STRATEGIES;STRATEGIES={
        0:always_defect,
        1:always_cooperate,
        2:random_defect,
        3:tit_for_tat
        4:friedman
        5:joss
    }
    message_text =  '''
                    0 - Always Defect
                    1 - Always Cooperate
                    2 - Random Defect
                    3 - Tit for Tat - will start coop, then do whatever opponent did last time
                    4 - Friedman - if opponent defects once, will keep defecting for rest of game
                    5 - Joss - coop first, then tit for tat but defects an additional 10% of the time
                    '''
    
    print("Welcome to a simulation of the prisoner's dilemma")
    while True:
        while(not(num_pattern.match(NUM_TURNS))):
            NUM_TURNS = input("How many turns do you want to simulate? [default 100]")
        while(not(num_pattern.match(strat_1))):
            strat_1 = input(message_text)
        while(not(num_pattern.match(NUM_TURNS))):
            strat_2 = input(message_text)
        simulate(NUM_TURNS, strat_1, strat_2)
    
def simulate(NUM_TURNS, strat_1, strat_2):
    print("Simulating for " + NUM_TURNS + " turns of "+ strat_1+ " vs "+ strat_2)
    score_1=0;score_2=0
    history = []
    print("P1 | P2")
    for i in range(NUM_TURNS):
        action_1 = STRATEGIES[strat_1](history, 1)
        action_2 = STRATEGIES[strat_2](history, 2)
        if(action_1==action_2):
            if(action_1==1): # both coop
                score_1+=3
                score_2+=3
            else: # both defected
                score_1+=1
                score_2+=1
        elif(action_1>action_2): # player 1 coop, player 2 defected
            score_2+=5
        else: # player 1 defected, player 2 coop
            score_1+=5
        print(" "+str(action_1) + " | "+ str(action_2))
        history.append((action_1, action_2))
        print("Strategy " + strat_1 +": "+score_1)
        print("Strategy "+strat_2+": "+score_2)


# strategies - returns 0 (defect) or 1 (cooperate)
# player refers to if you are the first or second player, relevant to some algorithms

def always_defect(history, player): 
    return 0

def always_cooperate(history, player):
    return 1

def tit_for_tat(history, player):
    if(len(history)==0):
        return(1)
    else:
        return(history[-1][player%1]) # fix this, this wrong
    
def random_defect(history, player):
    return(random.randint(0, 1))

def friedman(history, player):
    if(len(history)==0):
        return(1)
    elif((1,0) in history or (0,1) in history or (0,0) in history):
        return(0)
    else:
        return(1)
def joss(history, player):
    if(len(history)==0):
        return(1)
    else:
        if(history[-1][player%1]==1): # fix this, this wrong
            return 
    



            








