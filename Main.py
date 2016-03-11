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
    if(actions[0] is None):
        return actions
    else:
        choosenAct = eGreedyPicker(actions,state,features,player)
    
    return choosenAct

def step(state,player,act):
    state = dominoes.playGame(state,act,player)                  # do selected action
    print player + " played action : "+str(act)
    print "now state is " + str(state)
    return state

def evaluate(state,player,val,act,features,featureWeights,featuresVector):
    #A recompensa é dada após a ação dos 2 players
    #não é recompensa pela ação de 1 player, mas dos dois
    r = dominoes.reward(state,player)   
    next_action = policyAct(state,player,features)                  # choose next action
    # pega o novo valor e o utiliza para dar update
    new_value = qValue(state,next_action,features,player)
    target = r+ 0.9 * new_value                     # gamma = 0.9
    delta = target - val                            # prediction error
    #pra cada peso no array de caracteristicas aplica o gradient descent update
    #somente as caracteristicas validas no estado atual serão creditadas
    featureWeights += 0.5 * delta *featuresVector
    elements = [state,new_value,next_action,featureWeights]
    return elements

dominoes = Domino()
e = 0.01 # variavel global
featureWeights = np.zeros(20)
features = Features(0.01,1,featureWeights)
r = 0
duration = 0
state = dominoes.startGame()
print state
actionss1 = dominoes.possibleActions(state,"p1")
actP1 = policyAct(state,"p1",features)         # take action by a e-greedy policy
val1 = qValue(state,actP1,features,"p1")


while(dominoes.termination(state) == False):
    #self-play, onde o jogador joga consigo mesmo, avaliado e aprendendo somente
    #como p1, e utilizando o q-value para fazer as jogadas do p2
    featuresVector = features.featureValues(state,actP1,"p1")#salva vetor de carac antes de mudar
    state = step(state,"p1",actP1)
    print "valid features are: "+str(featuresVector)
    actionss2 = dominoes.possibleActions(state,"p2")
    actP2 = policyAct(state,"p2",features)
    state = step(state,"p2",actP2)

    #pega recompensas, atualiza as características e retorna novo
    #estado, valor e proxima acao
    state,val1,actP1,featureWeights =evaluate(state,"p1",val1,actP1,features,featureWeights,featuresVector)

print "weights: "+str(featureWeights)

