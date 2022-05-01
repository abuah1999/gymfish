# gymfish

> Refrain tonight,  
And that shall lend a kind of easiness  
To the next abstinence, the next more easy.   
>    **_Hamlet (3.4.167-9)_**

Gymfish is a simple re-inforcement learning algorithm made to solve the One-D chess puzzle originally published in Scientific American by Matthew
Gardner. For a complete explanation of the variant, the rules, and its solution, see this article: 
[https://www.linkedin.com/pulse/1d-chess-puzzle-brian-thomas/](https://www.linkedin.com/pulse/1d-chess-puzzle-brian-thomas/).

With best play, white can always achieve mate within 6 moves.

Starting with an agent that knows only the rules of the game and the relative values of the pieces, we train until
it is always able to punish sub-optimal play from the opponent and eventually achieves the optimal solution.

We trained in a custom environment made using OpenAI's ```openai.gym``` library. The learning algorithm uses a combination of self-play and q-table-based learning. These methods prove feasible given the reduced state-space of one-dimensional chess provided we choose a suitable reward function. In what follows, this will be the primary focus of our experimentation.
```
♜ - 5
♞ - 3
♚ - 100
```
We started with a simple material counting reward function using the above values. 
```
# Example game after 1500 training games (hereafter 'episodes')
♔♘♖..♜♞♚
♔♘...♖♞♚
```
Stalemate! Our fish greedily gobbles material and is unable to see far enough to a bigger reward. To stop the algorithm from 'bailing out' like this we set the reward function to return 0 given a board state which is a draw. It should be noted that setting the return value to a slightly negative value yields essentially the same behaviour and setting it to a negative value greater than the value of a piece makes the algorithm suicidal.
```
# Example game after 1500 episodes
♔♘♖..♜♞♚
♔.♖♘.♜♞♚
# so far so good...
♔.♖♘♞♜.♚
♔.♖.♞♘.♚
# our fish captured a rook with check - usually not a bad idea
♔.♖.♞♘♚.
# now the critical moment, will he find the right move?
.♔♖.♞♘♚.
# alas... The move isn't as silly as it seems however - if black captures the knight white can just move the rook up one
# the black knight is then pinned and cannot move, black's only move is with the king back and then mate to follow.
# In another line, if white had played rook to a2 then black knight to a3 check leads to a draw after rook takes knight.
# The correct move is Ra4.
```
The agent is unable to look deeply enough to see a forced mate in 3. A deep learning network taking the place of our q-table might do the job. For now, we will try to amend our reward function to make it less sparse. This way at least, when our algorithm needs to see a longer sequence of moves as in the last case it will not be shooting in the dark. One possible solution may be to count space (#legal white moves - #black legal moves) as well as material.
