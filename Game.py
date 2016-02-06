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
    
    
def play(state,action):
    
    #play
    #action[0] = se é uma jogada, action[1] = peça em si,
    #action[2]= pos da peça na mão
    if(action[0]==1):
       
        field_pieces = state.pop(2)
        hand = state.pop(0)
        pos = action[1]
        if(pos<0 or pos > len(hand)):
            print "posicao invalida"
            state.insert(1,field_pieces)    
            state.insert(0,hand)
            return state
       
        piece = hand[pos]
        orientation = action[2]#se é a esq(0) ou dir(1) da peça q importa
        piece_value = piece[orientation]
        if(len(field_pieces)>0):
            #pega a 1 peça e seu valor a esq
            first = field_pieces[0]
            leftmost_value = first[0]
            #pega a ultima peça e seu valor a dir
            last = field_pieces[-1]
            rightmost_value = last[1]
            print "piece value ",piece_value
            print "r ",rightmost_value, " l ", leftmost_value
            if(piece_value==leftmost_value ):
                if(orientation == 0):
                    hand.remove(piece)
                    new_piece = (piece[1],piece[0]) #recebe peça invertida
                    field_pieces.insert(0,new_piece)
                else:
                    hand.remove(piece)
                    field_pieces.insert(0,piece)
                                
            elif(piece_value == rightmost_value): 
                if(orientation == 1): #recebe peça invertida
                    hand.remove(piece)
                    new_piece = (piece[1],piece[0])
                    field_pieces.append(new_piece)
                else:
                    hand.remove(piece)
                    field_pieces.append(piece)
            else:
                print "Peça não é válida"
                
        else:
            hand.remove(piece)
            field_pieces.insert(0,piece)
            
    state.insert(1,field_pieces)    
    state.insert(0,hand)  
    return state
        
    #pass

#Start a game of dominoes, shuffling pieces and giving 7 to each player
def initGame():
    status = 1 #1=in progress; 2=player won; 3=draw; 4 = dealer won/player loses
    #peca tem seu valor como tupla, e orientacao,
    #por exem: [(1,0),0] = (1,0) e  [(1,0),1] = (0,1)
    pieces = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]
    random.shuffle(pieces)
    player_hand = []
    dealer_hand = []
    player_hand = take_initial_pieces(player_hand,pieces)
    dealer_hand = take_initial_pieces(dealer_hand,pieces)
    field_pieces = []
    #retorna estado do jogo total
    state = [player_hand,dealer_hand,field_pieces,pieces,status]
    return state
