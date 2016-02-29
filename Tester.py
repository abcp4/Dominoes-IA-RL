state = initGame()
print state[0]
actionSet=possibleActions(state)#pede uma lista de ações possiveis
actions_index = actionSet[1]
state = playGame(state,actions_index[0])#joga uma das ações possiveis, no começo sao todas
print state
actionSet=possibleActions(state)#pede uma lista de ações possiveis
actions_index = actionSet[1]
print actions_index
state = playGame(state,actions_index[0])#joga uma das ações possiveis
print state
