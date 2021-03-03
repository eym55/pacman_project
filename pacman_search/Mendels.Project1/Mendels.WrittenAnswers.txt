# Write Up

## Question 4: What happens when you run A* on OpenMaze with the Manhattan Heuristic?

When running each search on the open maze, BFS, UCS and A* all of them found an optimal path. However, A* only explored 535 nodes as opposed to 682 making it significantly more efficient. 

## Question 5: What did you choose to include in your game state? Why? How many nodes does BFS expand in your representation?

I chose to use a tuple that contains both the coordinates of Pacman as well as a tuple of unseen corners. I used tuples because I had originally used sets and needed an immutable object. I included both the position and the seen corners because to check if a state is a goal I needed to check whether the state has seen all the corners but to get the adjacent nodes I needed the actual coordinates. In the medium maze my search explored 2448 nodes. This is more than I was expecting but not a significant difference as it still ran instantly.

## Question 6: What did you choose as a heuristic? Why? Argue (i.e., prove) why it is admissible. How many game states did it explore?

For my heuristic I chose the sum of the manhattan distance from the state to the closest corner, and then the distance of the next closest corner for each corner that hadn't been seen. The heuristic is clearly admissible because the manhattan distance between two points is a lower bound for the maze distance. From a corner, the shortest distance to the remaining corners is along the edges in a straight line to each corner that hasn't been seen. Therefore, the shortest possible path would be bound below by the manhattan distance to the closest corner plus the manhattan distance from there to each successive corner where the position is updated to match the current corner. Since the heuristic represents a lower bound for the actual distance, it can't overestimate it and is admissible. My heuristic expanded only 908 nodes. 

## Question 7: What did you choose as a heuristic? Why? Argue (i.e., prove) that it is consistent. How many game states did it explore?

For this problem I chose the maximum maze distance to a food dot as my heuristic. I tried a variety of heuristics and found that the upper bound appeared to be the distance to the farthest dot and it was more effective the closer I was to that bound. I then found the mazedistance function and tested it and found that it was more effective than the manhattan distance function. If there are no more food nodes, it returns 0 which is consistent for a goal state. It increased the runtime significantly but also lowered the nodes expanded significantly to 4137 nodes in 38.3 seconds. Note that if I had used the similarly consistent manhattan distance function it wouldve been about 9000 nodes in under 5 seconds. This heuristic is consisistent because of the definition of consistency. For every node N and successor P, the heuristic is less than or equal too the cost of getting to P and the heuristic of P. The condition of h(G) = 0 is clearly satisfied. For the primary condition it is clear that h(N) = the distance between N and the farthest food node. For P the heuristic is the distance from P to the farthest food node. The cost is equal to the distance from N to P and since the state is updated to move the distance of that cost and the final state is P, the distance from P to G cannot be less than h(N) - Cost. This makes the heuristic consistent.

## Question 8: Describe a condition or a small example where ClosestDotSearchAgent will fail.

The search agent will fail if there is a food dot that is inaccessible to the Pacman. If there was food enclosed entirely in walls, then the problem would run indefinitely and never reach a goal state. 