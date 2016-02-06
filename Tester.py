state = initGame()
print state[0]
action = [1,0,0] #se é jogada,pos da peça na mão, lado da peça
play(state,action)
print "hand after: ", state[0]
print "field after: ", state[2]
