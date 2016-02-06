import math
import random
from random import shuffle


def take_initial_pieces(hand,pieces):
    n = 0
    while(n<7):
        hand.append(pieces[n])
        #print pieces[n]
        n= n+1
    del pieces[0:7]
    return hand
    
    
def play(state action):
    

#Start a game of dominoes, shuffling pieces and giving 7 to each player
def initGame():
    status = 1 #1=in progress; 2=player won; 3=draw; 4 = dealer won/player loses
    
    pieces = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]
    random.shuffle(pieces)
    player_hand = []
    dealer_hand = []
    player_hand = take_initial_pieces(player_hand,pieces)
    dealer_hand = take_initial_pieces(dealer_hand,pieces)
    field_pieces = []
    #retorna estado visivel ao jogador:
    #sua mão,peças no campo(0 inicialmente), estado do jogo 
    #seria aqui o vetor de caracteristicas? 
    #tudo que for util para representar o estado?
    state = (player_hand, field_pieces,status)
    return state
