# gymfish

> Refrain tonight,  
And that shall lend a kind of easiness  
To the next abstinence, the next more easy.   
>    **_Hamlet (3.4.167-9)_**

A simple re-inforcement learning algorithm to solve the One-D chess puzzle originally published in Scientific American by Matthew
Gardner. For a complete explanation of the variant, the rules, and its solution, see this article: 
[https://www.linkedin.com/pulse/1d-chess-puzzle-brian-thomas/](https://www.linkedin.com/pulse/1d-chess-puzzle-brian-thomas/).

With best play, white can always mate within 6 moves.

Starting with an agent that knows only the rules of the game and the relative values of the pieces, we train until
it is always able to punish sub-optimal play from the opponent and eventually achieves the optimal solution.

We trained in a custom environment made using OpenAI's ```openai.gym``` library. The learning algorithm 
