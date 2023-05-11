How to run: 
1. Terminal: python3 MapQuest_112.py
2. VSCode: Press play button

Algorithms: 
1. Min Max Model: The algorithm takes into account all the possible moves that players can take at any given time during the game. It keeps playing ahead until it reaches a terminal arrangement of the board (terminal state) resulting in a tie, a win, or a loss. Once in a terminal state, the AI will assign an arbitrary positive score (+10) for a win, a negative score (-10) for a loss, or a neutral score (0) for a tie. At the same time, the algorithm evaluates the moves that lead to a terminal state based on the players’ turn. It will choose the move with maximum score when it is the AI’s turn and choose the move with the minimum score when it is the human player’s turn.
2. Floyd-Washall: The algorithm finds the shortest paths between pairs of vertices in a graph. It takes into account the moving units on the map and finds the shortest path between any two locations. Ultimately, this allows the AI to make the best decision on how to attack the player. 

MVC Programming Style: MVC, or Model-View-Controller, is a software architectural pattern that separates an application into three interconnected components: the Model, the View, and the Controller. This separation of concerns allows for a clear division of labor and improved maintainability.

The Model represents the underlying data and business logic of the application. It is responsible for managing the data and enforcing any constraints or rules on that data.

The View is responsible for presenting the data to the user. It retrieves data from the Model and displays it in a format that is appropriate for the user interface.

The Controller acts as an intermediary between the Model and View. It receives input from the user, processes it, and updates the Model and/or View accordingly.

By separating these concerns into distinct components, MVC allows for greater flexibility and modularity in software design. Each component can be developed and tested independently, making it easier to maintain and update the application over time.

Improvements: The game could utilize more sophisticated metrics for deciding on how to have the AI attack the player. For instance, instead of using randomness to instantiate the AI's possible moves, a sort of bias could be added to them to allow for more calculated and a much more signature play-style against the player. Additionally, the implementation of machine learning into the AI could create for an interesting opponent that could learn from the player as the game progresses, which could make the analysis of game strategy yield much more interesting results. Using the resources of a super-computer cluster would allow for more simulations to be run and ultimately develop the best possible machine learning model for the AI. 
