import gym
import math
#import numpy as np

class OneDChessEnvironment(gym.Env):
    """A 1-D Chess environment for OpenAI gym"""

    worth = {"K": 1000010, "R": 500, "N": 300, "k": -1000010, "r": -500, "n": -300, ".": 0}

    def insufficient_material(self):
        count = 0
        for c in self.board:
            if c == ".":
                count += 1
        return count == 6

    def is_check(self, board):
        i = board.index("K")
        is_king_check = (i+1 < 8 and board[i+1] == "k") or (i-1 > -1 and board[i-1] == "k")
        is_knight_check = (i+2 < 8 and board[i+2] == "n") or (i-2 > -1 and board[i-2] == "n")
        is_rook_check = False
        for d in (1,-1):
            j = i + d
            while j < 8 and j > -1:
                if board[j]==".":
                    j += d
                elif board[j]=="r":
                    is_rook_check = True
                    break
                else:
                    break         
        return is_king_check or is_knight_check or is_rook_check

    def append_move(self, moveList, move, board):
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        new_board = put(board, move[1], board[move[0]])
        new_board = put(new_board, move[0], ".")
        if not self.is_check(new_board):
            moveList.append(move)
        else:
            pass


    def legal_moves(self):
        moves = []
        board = self.board
        for i in range(len(board)):
            if board[i] == "K":
                if i+1 < 8 and not board[i+1].isupper():
                    self.append_move(moves, (i, i+1), board)
                if i-1 > -1 and not board[i-1].isupper():
                    self.append_move(moves, (i, i-1), board)
            if board[i] == "N":
                if i+2 < 8 and not board[i+2].isupper():
                    self.append_move(moves, (i, i+2), board)
                if i-2 > -1 and not board[i-2].isupper():
                    self.append_move(moves, (i, i-2), board)
            if board[i] == "R":
                for d in (1,-1):
                    j = i + d
                    while j < 8 and j > -1:
                        if board[j]==".":
                            self.append_move(moves, (i, j), board)
                        elif board[j].islower():
                            self.append_move(moves, (i, j), board)
                            break
                        else:
                            break
                        j += d
        return moves

    def flip(self):
        self.board = self.board[::-1].swapcase()

    def _next_observation(self):
        return self.observation_map[self.board]

    def reset(self):
        self.step_stack = []
        self.board = "KNR..rnk"
        self.balance = sum([self.worth[x] for x in self.board])
        return self._next_observation()

    def __init__(self):
        super().__init__()
        self.step_stack = []
        self.board = "KNR..rnk"
        self.balance = sum([self.worth[x] for x in self.board])
        self.reward_range = (-math.inf, math.inf)
        self.observations = ["........"]

        put = lambda board, i, p: board[:i] + p + board[i+1:]
        for p in "KNRknr":
            new_list = []
            for s in self.observations:
               for i in range(len(s)):
                   if s[i] == ".":
                       new_list.append(put(s, i, p))
            self.observations += new_list

        self.observation_map = {}

        for i, s in enumerate(self.observations):
            self.observation_map[s] = i

        self.action_space = gym.spaces.Discrete(9)
        self.observation_space = gym.spaces.Discrete(len(self.observations))

    def step(self, action):
        moves = self.legal_moves()
        #print(len(moves))
        action = action % len(moves)
        self._take_action(moves[action])
        reward = self.balance
        self.flip()
        obs = self._next_observation()
        self.balance = -self.balance
        reward = -500 if len(self.legal_moves())==0 or (self.balance, self.board) in self.step_stack or self.insufficient_material() else reward
        done = reward > 1000000 or reward < -1000000 or len(self.legal_moves())==0 or self.insufficient_material() or (self.balance, self.board) in self.step_stack
        self.step_stack.append((self.balance, self.board))
        return obs, reward, done, {}

    def pop(self):
        self.step_stack.pop()
        self.board = self.step_stack[-1][1]
        self.balance = self.step_stack[-1][0]

    def _take_action(self, action):
        p = self.board[action[0]]
        q = self.board[action[1]]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        if (q.islower()):
            self.balance -= self.worth[q]
        self.board = put(self.board, action[1], p)
        self.board = put(self.board, action[0], ".")
        

    def render(self):
        uni_pieces = {'R':'♜', 'N':'♞', 'K':'♚', 
                  'r':'♖', 'n':'♘','k':'♔','.':'·'}
        board = [uni_pieces[x] for x in self.board]
        print("".join(board))