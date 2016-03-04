import random
import numpy as np
import scipy


e = 0.01 # epsilon-greedy proportion

num_features = 60
featureWeights = np.zeros(numFeatures)

beta = 50.0
features = Features()
     
def qValue(state,act):
    featureVals = features.featuresValue(state,act)
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

        

        new_value = numpy.dot (featureWeights, featureVals)     # value after action
        target = r+ 0.9 * new_value                     # gamma = 0.9
        delta = target - val                            # prediction error

        featureWeights += 0.5 * delta * numpy.outer (act_vec, I) #pra cada peso no array de caracteristicas aplica o gradient descent update

        state = next_state
        val = new_value
        act = next_action
        
