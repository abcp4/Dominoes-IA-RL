import random
import numpy as np


e = 0.01 # epsilon-greedy proportion

numFeatures = 20
featureWeights = np.zeros(numFeatures)

beta = 50.0
class Features:

    def featureValues(self,state,action):
        numFeatures = 20
        hand = state[1]
        l_end = state[4]
        r_end = state[5]
        pos = action[2]
        result =  np.zeros(numFeatures)
        if(l_end==r_end==-1):
            pos = action[4]
            l_end = action[0]
            r_end = action[2]
        elif(action[1]=="left"):
        #substitui uma das pontas pela nova ação
            l_end = action[0]
        else:
            r_end = action[0]
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
    
features = Features()

def qValue(state,act):
    featureVals = features.featureValues(state,act)
    val = numpy.dot (featureWeights, featureVals)    # value before action
    return val
        
def eGreedyPicker(actions,state):
    rand = np.random.random_sample()
    bestValue = 0
    if(rand > e):
        for act in actions:
            value = qValue(state,act)
            if(value> bestValue):
                bestValue = value
        choosenAct = bestValue
    else:
        choosenAct = random.choice(actions)
        
    return choosenAct

def policyAct(state):
    actions = dominoes.possibleActions(state)
    #escolhe a partir dos valores na q-value com tecnica e-greedy
    choosenAct = eGreedyPicker(actions,state)
    
    return choosenAct


for iter in range (10000):
    
    state = dominoes.startGame() 
    act = policyAct (state)                         # take action by a e-greedy policy
    val = qValue(state,act)
    r = 0
    duration = 0
    while dominoes.termination() == 0:

        dominoes.act(act)                                  # do selected action
        r = dominoes.reward()                              # read reward

        next_state = dominoes.state()                   # read new state
        next_action = policyAct(state)                  # choose next action

        
        # value after action
        new_value = numpy.dot(featureWeights,features.featuresValue(state,act))
        target = r+ 0.9 * new_value                     # gamma = 0.9
        delta = target - val                            # prediction error
        
        #pra cada peso no array de caracteristicas aplica o gradient descent update
        #somente as caracteristicas validas no estado atual serão creditadas
        featureWeights += 0.5 * delta *features.featuresValue(state,act) 

        state = next_state
        val = new_value
        act = next_action
        
