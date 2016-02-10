import math
import random
from random import shuffle

def buy(hand, n, pieces):
    i = 0
    while i<n:
        hand.append(pieces[i])
        i=i+1
    del pieces[0:n]
    return hand

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

def playGame(state, p_index):
    status = state[0]
    p1_hand = state[1]
    p2_hand = state[2]
    field = state[3]
    l_end = state[4]
    r_end = state[5]

    if status==1:
        #assumindo que p_index foi escolhido corretamente por outra funcao
	#o certo seria chamar a funcao que escolhe p_index aqui, mas como ela nao foi feita, fica essa gambiarra ae :P
        p = p1_hand[p_index]
        field.append(p)
        p1_hand.remove(p)
        if (l_end==-1 & r_end==-1):
            l_end, r_end = p
        elif (l_end==p[0]):
            l_end=p[1]
        elif (l_end==p[1]):
            l_end=p[0]
        elif (r_end==p[0]):
            r_end=p[1]
        elif (r_end==p[1]):
            r_end=p[0]
        #a partir daqui eh a escolha do oponente
    state = [status, p1_hand, p2_hand, field, l_end, r_end]
    return state
