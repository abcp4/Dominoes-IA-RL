import random
import numpy as np

class Features:
    
    def __init__(self,epsilon,beta,featureWeights):
        self.data = []
        e = epsilon # epsilon-greedy proportion
        self.beta = beta
        self.featureWeights = featureWeights
        
    def getFeaturesWeights(self):
        return self.featureWeights
    
    def featureValues(self,state,action,player):
        numFeatures = 20
        if(player == "p1"):
            hand = state[1]
        elif(player == "p2"):
            hand = state[2]
        l_end = state[4]
        r_end = state[5]
        pos = action[2]
        result =  np.zeros(numFeatures)
        if(l_end==r_end==-1):
            pos = action[2]
            l_end = action[0]
            r_end = action[1]
        elif(action[1]=="left"):
        #substitui uma das pontas pela nova ação
            l_end = action[0]
        else:
            r_end = action[0]
        print "pos: "+str(pos)
        value =hand.pop(pos)
        """
        Características a partir de informações imperfeitas.
            Somente do que é visível a um jogador comum:
                Campo, peças de suas mãos, quantidade de peças do oponente
        """
        #valida caracteristicas de acordo com o estado submetido e as retorna
        
        result[0] = self.NumDouble(hand,action,l_end,r_end,lambda x: x==1)
        result[1] = self.NumDouble(hand,action,l_end,r_end,lambda x: x==2)
        result[2] = self.NumDouble(hand,action,l_end,r_end,lambda x: x>=3)
        #impossibilita qualquer peça de ser jogada
        result[3] = self.blocksMe(hand,action,l_end,r_end)
        
        result[4] = self.NumActions(hand,action,l_end,r_end,lambda x: x==1)
        result[5] = self.NumActions(hand,action,l_end,r_end,lambda x: x==2)
        result[6] = self.NumActions(hand,action,l_end,r_end,lambda x: x>=3)
        
        for i in range(7,14):
            #quais peças duplas temos na mão, de 0:0 a 6:6
            result[i] = self.hasDouble(i-7,hand,action)
        
        """
        Características a partir de informações perfeitas.
        Sabe-se da mão do oponente, de toda e qualquer informação necessária
        para se tomar uma decisão
        """
        
        hand.insert(pos,value)
        
        return result
    
    def NumDouble(self,hand,action,l_end,r_end,exp):
        count = 0
        for piece in hand:
            if(piece[0] == piece[1]):
                count +=1
        if(exp(count)):
            return True
        return False
    
    def hasDouble(self,number,hand,action):
        for piece in hand:
            if((piece[0] == piece[1]) and (piece[0] == number)):
                return True
        return False
    
    def blocksMe(self,hand,action,l_end,r_end):      
        for piece in hand:
            if(self.isPlayable(piece,l_end,r_end)):
                #se encontra alguma peça valida na mao
                return False # então ainda não estou bloqueado
  
        return True #nao encontrou
        
    def NumActions(self,hand,action,l_end,r_end,exp):
        count = 0
        for piece in hand:
            if(self.isPlayable(piece,l_end,r_end)):
                count +=1
        if(exp(count)):#se tem mais que o numero de peças designado
            return True
        return False #se tem exatamente aquele numero
          
    def isPlayable(self,piece,l_end,r_end):#se dado a peça e as duas pontas, ela é jogavel
        if(piece[0]==l_end or piece[0]==r_end or piece[1]==l_end or piece[1]==r_end):
               return True
        return False
    
#dado o jogador, sua acao, o estado e suas caracteristicas, retorne o valor dessa acao
#e necessario diferencia os jogadores pois ele precisa examinar 2 hands 
#o act n especifica de que hand e
def qValue(state,act,features,player):
    featureVals = features.featureValues(state,act,player)
    val = np.dot (features.getFeaturesWeights(), featureVals)    # value before action
    return val
        
def eGreedyPicker(actions,state,features,player):
    rand = np.random.random_sample()
    bestValue = -999999 #tomar cuidado aqui
    if(rand > e):
        for act in actions:
            value = qValue(state,act,features,player)
            if(value> bestValue):
                bestValue = value
                choosenAct = act
    else:
        choosenAct = random.choice(actions)
        
    return choosenAct

def policyAct(state,player,features):
    actions = dominoes.possibleActions(state,player)
    #escolhe a partir dos valores na q-value com tecnica e-greedy
    choosenAct = eGreedyPicker(actions,state,features,player)
    
    return choosenAct
