import random, re
from termcolor import colored

def main():
    num_pattern = re.compile("^[0-9]+$")
    alpha_pattern = re.compile("^[A-Za-z]+$")
    global NUM_TURNS; 
    global STRATEGIES;STRATEGIES={
        0:always_defect,
        1:always_cooperate,
        2:random_defect,
        3:tit_for_tat,
        4:friedman,
        5:joss
    }
    message_text ='''
    0 - Always Defect - Only defects.
    1 - Always Cooperate - Only cooperates.
    2 - Random Defect - Defects 50% of the time.
    3 - Tit for Tat - Will start by cooperating, then will do whatever opponent did last time.
    4 - Friedman - If the opponent defects once, it will keep defecting for rest of game.
    5 - Joss - Tit for Tat but defects an additional 10% of the time.
    '''
    keep_going = True
    print("Welcome to a simulation of the prisoner's dilemma")
    
    while keep_going:
        NUM_TURNS = ""
        strat_0=""
        strat_1=""
        while(not(num_pattern.match(str(NUM_TURNS)))):
            NUM_TURNS = input("How many turns do you want to simulate? [default 100]")
        while(not(num_pattern.match(str(strat_0)) and int(strat_0) in STRATEGIES)):
            strat_0 = input(message_text)
        while(not(num_pattern.match(str(strat_1)) and int(strat_1) in STRATEGIES)):
            strat_1 = input(message_text)
        NUM_TURNS = int(NUM_TURNS)
        strat_0 = int(strat_0)
        strat_1 = int(strat_1)
        simulate(NUM_TURNS, strat_0, strat_1)
        k = input("Run another simulation? [y/Y to keep going, any char to stop]")
        if(not(k == 'y' or k =='Y')):
            keep_going = False
    
def simulate(NUM_TURNS, strat_0, strat_1):
    print("Simulating for " + str(NUM_TURNS) + " turns of "+ STRATEGIES[strat_0].__name__ + " vs "+ STRATEGIES[strat_1].__name__)
    score_0=0;score_1=0
    history = []
    print("P1 | P2")
    for i in range(NUM_TURNS):
        action_0 = STRATEGIES[strat_0](history, 0)
        action_1 = STRATEGIES[strat_1](history, 1)
        if(action_0==action_1):
            if(action_0==1): # both coop
                score_0+=3
                score_1+=3
            else: # both defected
                score_0+=1
                score_1+=1
        elif(action_0>action_1): # player 0 coop, player 1 defected
            score_1+=5
        else: # player 0 defected, player 1 coop
            score_0+=5
        print(" "+str(action_0) + " | "+ str(action_1))
        history.append((action_0, action_1))
    print("Strategy " + STRATEGIES[strat_0].__name__ +": "+str(score_0)+"/"+str(NUM_TURNS*5))
    print("Strategy "+STRATEGIES[strat_1].__name__+": "+str(score_1)+"/"+str(NUM_TURNS*5))


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
        return(history[-1][player^1]) # the idea of player^1 is to get 0 if 1, 1 if 0
    
def random_defect(history, player):
    return(random.randint(0, 1))

def friedman(history, player):
    if(len(history)==0):
        return(1)
    elif((1,0) in history or (0,1) in history or (0,0) in history):
        return(0)
    else:
        return(1)

def joss(history, player): # greedy tit for tat
    if(len(history)==0):
        return(1)
    else:
        if(history[-1][player^1]==1): 
            return (0 if random.randint(0,9)==0 else 1)
        else:
            return 0

if __name__ == "__main__":
    main()
