import numpy as np

def is_check(board):
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

print(is_check(".NR.K.nk"))