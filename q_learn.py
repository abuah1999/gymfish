from webbrowser import get
from oned_chess import OneDChessEnvironment
import numpy as np 

# 1. Load Environment and Q-table structure
env = OneDChessEnvironment()
Q = np.zeros([env.observation_space.n,env.action_space.n])
# env.observation.n, env.action_space.n gives number of states and action in env loaded
# 2. Parameters of Q-learning
eta = .628
gma = .9
epis = 50000
rev_list = [] # rewards per episode calculate
# 3. Q-learning Algorithm
for i in range(epis):
    # Reset environment
    s = env.reset()
    rAll = 0
    d = False
    j = 0
    #The Q-Table learning algorithm
    while not d:
        #env.render()
        # Choose action from Q table
        a = np.argmax(Q[s,:] + np.random.randn(1,env.action_space.n)*(200./(i+1)))
        n = len(env.legal_moves())
        #Get new state & reward from environment
        s1,r,d,_ = env.step(a)
        if not d:
            a2 = np.argmax(Q[s1,:] + np.random.randn(1,env.action_space.n)*(200./(i+1)))
            s2,_,_,_ = env.step(a2)
            #Update Q-Table with new knowledge
            while a > -1:
                Q[s,a] = Q[s,a] + eta*(r + gma*np.max(Q[s2,:]) - Q[s,a])
                a -= n
            env.pop()
        else:
            #Update Q-Table with new knowledge
            while a > -1:
                Q[s,a] = Q[s,a] + eta*(r - Q[s,a])
                a -= n
        rAll += r
        s = s1
        #env.render()
    rev_list.append(rAll)
    #env.render()
print("Reward Sum on all episodes " + str(sum(rev_list)/epis))

def get_user_input(env):
     print("enter your move: ")
     user_move = str(input())
     #user_move = user_move.split()
     #user_move = tuple(user_move)
     user_move = (int(user_move[0]), int(user_move[1]))
     try:
         return env.legal_moves().index(user_move)
     except:
         print("please enter a legal move")
         return get_user_input(env)

done = False
env = OneDChessEnvironment()
s = env.reset()
user_turn = False

while (not done):
    if user_turn:
        env.render()
        user_action = get_user_input(env)
        s,_,done,_ = env.step(user_action)
    else:
        q_action = a = np.argmax(Q[s,:])
        s,_,done,_ = env.step(q_action)
    user_turn = not user_turn
#env.render()
if len(env.legal_moves()) == 0 and not env.is_check(env.board):
    print("draw.")
elif user_turn:
    print("better luck next time...")
else:
    print("you won!")
