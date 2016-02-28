import math
import random
from random import shuffle

#O ambiente pode ser feito em puro python, não precisa de alto tempo de resposta, nem faz processamento pesado

def buy(hand, n, pieces):
    i = 0
    while i<n:
        hand.append(pieces[i])
        i=i+1
    del pieces[0:n]
    return hand
    
#recebe estado do jogo, retorna ações possíveis
def possibleActions(state):
    l_end = state[4]
    r_end = state[5]	
    hand = state[1]
    actions = []
    actions_index = []
    actionSet= []
    index = 0
    for piece in hand:
    	index +=1
    #peça dupla
    	if(piece[0]==piece[1]):
        	if(piece[0]==l_end):
                	actions.append((piece[1],"left"))
                	actions_index.append((index,1))
        	elif(piece[1]==r_end):
            		actions.append((piece[0],"right"))
            		actions_index.append((index,0))
        	continue
    
    	if(piece[0]==l_end):
    		actions.append((piece[1],"left"))
    		actions_index.append((index,1))
        	if(l_end==r_end): #evitar duplicacao de mesmas ações na esq e dir
            		continue
    	if(piece[1]==l_end):
    		actions.append((piece[0],"left"))
    		actions_index.append((index,0))
        	if(l_end==r_end):
        		continue
    
    	if(piece[0]==r_end):
    		actions.append((piece[1],"right"))
    		actions_index.append((index,1))
        	if(l_end==r_end):
            		continue
    	if(piece[1]==r_end):
    		actions.append((piece[0],"right"))
    		actions_index.append((index,0))
        	if(l_end==r_end):
            		continue
       
    actionSet = [actions,actions_index]		
    return actionSet

def startGame():
    status = 1 #1=in progress; 2=player won; 3=draw; 4 = dealer won/player loses
    pieces = [(x,y) for x in range(7) for y in range(x,7)]
    random.shuffle(pieces)
    p1_hand = buy([],7,pieces)
    p2_hand = buy([],7,pieces)
    field = []
    l_end = -1
    r_end = -1
    state = [status, p1_hand, p2_hand, field, l_end, r_end]
    return state

def playGame(state, p_index,orientation):
    status = state[0]
    p1_hand = state[1]
    p2_hand = state[2]
    field = state[3]
    l_end = state[4]
    r_end = state[5]

    if status==1:
        p = p1_hand[p_index]
        field.append(p)
        p1_hand.remove(p)
        if (l_end==-1 and r_end==-1):
            l_end, r_end = p
        elif (l_end==p[0] and orientation == 0):
            l_end=p[1]
        elif (l_end==p[1] and orientation == 1):
            l_end=p[0]
        elif (r_end==p[0] and orientation == 0):
            r_end=p[1]
        elif (r_end==p[1] and orientation == 1):
            r_end=p[0]
        #a partir daqui eh a escolha do oponente
    state = [status, p1_hand, p2_hand, field, l_end, r_end]
    return state
