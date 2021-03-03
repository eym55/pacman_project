# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.

	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"
		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"

		#Breaking the function into two parts, food and enemies and then combining them into one value
		#I started with my food distance heurisitc from project 2 but then played around with it, switching to min distance and adding a factor of the food_count
		food_locations = [(x,y) for x in range(newFood.width) for y in range(newFood.height) if newFood[x][y] == True]
		food_score = 1
		if food_locations:
			new_food_count = len(food_locations)
			food_dist = sum([util.manhattanDistance(newPos, food) for food in food_locations])
			food_score = food_dist*new_food_count**8
		"Ghost Score part"
		ghost_score = 1
		for ghost_dist in [util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]:
			if ghost_dist < 4:
				ghost_score *= (5-ghost_dist)**4
			if min(newScaredTimes)>min([util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]):
				ghost_score *= -1



		return -food_score*ghost_score

def scoreEvaluationFunction(currentGameState):
	"""
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.

	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.

		Here are some method calls that might be useful when implementing minimax.

		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1

		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action

		gameState.getNumAgents():
		Returns the total number of agents in the game

		gameState.isWin():
		Returns whether or not the game state is a winning state

		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		"*** YOUR CODE HERE ***"
		#Helper variables for checking depths and agent indices.
		num_agents = gameState.getNumAgents()
		max_depth = self.depth * num_agents
		#The following code follows from the psuedocode implementation on the slides but has been modified
		#Function to run minimax
		def minimax_decision(gameState):
			return maxValue(gameState,0)[1]
		
		#Function for calulcating the value of a max node
		def maxValue(state,depth):
			#Getting the agent index from the depth
			agent_index = depth % num_agents
			#Return the evaluation if the node is a leaf
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state),None)
			value = -float('inf')
			action = None
			#Get the maximum of the nodes below it and return the value and action in a pair
			for a in state.getLegalActions(agent_index):
				temp = minValue(state.generateSuccessor(agent_index, a),depth+1)[0]
				if  temp > value:
					value = temp
					action = a
			return (value, action)
		#Function for calulcating the value of a min node, same as above except for the modification for extra ghosts
		def minValue(state,depth):
			agent_index = depth % num_agents
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state),None)
			value = float('inf')
			action = None
			for a in state.getLegalActions(agent_index):
				#Check whether the next node is a max or a min and use the correct evaluation function
				if (agent_index+1)%num_agents == 0:
					temp = maxValue(state.generateSuccessor(agent_index, a),depth+1)[0]
				else:
					temp = minValue(state.generateSuccessor(agent_index, a),depth+1)[0]
				
				if  temp < value:
					value = temp
					action = a
			return (value, action)

		#Helper function to check terminal states
		def isTerminalState(state,depth):
			if depth >= max_depth or state.isWin() or state.isLose():
				return True
			else:
				return False

		return minimax_decision(gameState)
		"I left my first implementation below because I spent most of my time on it before switching to one based off of the slides"
		"I also spoke to Matt Catalano about how he structured his response which led me to swtich to the implementaion based off the lecture slides"
		"My code below was partially inspired by this implementation: https://www.baeldung.com/java-minimax-algorithm"
		#Storing the total number of agents and the maximum depth for later use
		#Helped function to check if a node should have any children

		#Node class to store information about states
		#Each node stores the depth, agent index, score, action to get there the state and a list of child nodes
		# class Node():
		# 	def __init__(self,depth,agent,state,children = [], score = None, action = None):
		# 		self.depth = depth
		# 		self.score = score
		# 		self.agent = agent
		# 		self.children = children
		# 		self.state = state
		# 		self.action = action

		# 	def add_child(self,node):
		# 		self.children.append(node)

		# 	def set_score(self,score):
		# 		self.score = score

		# 	def get_score(self):
		# 		if self.score is not None:
		# 			return self.score
		# 		if self.isTerminalState():
		# 			print(self.state.isWin() and self.state.isLose())
		# 			return evaluationFunction(self.state)
		# 		elif self.agent == 0:
		# 			return max([child.get_score() for child in self.children])
		# 		elif self.agent >= 1:
		# 			return min([child.get_score() for child in self.children])

		# 	def get_best_action(self):
		# 		ba = None
		# 		max_score = -float("inf")
		# 		for child in self.children:
		# 			score = child.get_score()
		# 			if score >= max_score:
		# 				max_score = score
		# 				ba = child.action
		# 		print(max_score)
		# 		return ba
		# 	def isTerminalState(self):
		# 		if self.depth >= max_depth or self.state.isWin() or self.state.isLose():
		# 			return True
		# 		else:
		# 			return False


		# #Tree for the game tree
		# class Tree():
		# 	def __init__(self,root=None):
		# 		self.root = root

		# root = Node(0,0,gameState)
		# tree = Tree(root)
		# def buildTree(parent):
		# 	new_depth = parent.depth+1
		# 	new_agent = (parent.agent + 1) % self.depth
		# 	actions = parent.state.getLegalActions(parent.agent)
		# 	curr_state = parent.state
		# 	for new_state, action in [(curr_state.generateSuccessor(parent.agent, action), action) for action in actions]:
		# 		new_node = Node(new_depth,new_agent,new_state, action = action)
		# 		parent.add_child(new_node)
		# 		if new_node.isTerminalState():
		# 			new_node.set_score(evaluationFunction(new_state))
		# 			if parent.score==None:
		# 				parent.score = new_node.score
		# 			if parent.agent == 0 and parent.score < new_node.score:
		# 				parent.score = new_node.score
		# 			elif parent.agent >= 0 and parent.score > new_node.score:
		# 				parent.score = new_node.score
		# 		else:
		# 			buildTree(new_node)		
		# 		if parent.score==None:
		# 			parent.score = new_node.score
		# 		if parent.agent == 0 and parent.score < new_node.score:
		# 			parent.score = new_node.score
		# 		elif parent.agent >= 1 and parent.score > new_node.score:
		# 			parent.score = new_node.score
		# 			#new_node.set_score(new_node.get_score())
					

		# buildTree(tree.root)
		# print('Tree is done')
		# return tree.root.get_best_action()

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		#The same as above but modified for alpha-beta
		#Helper variables for checking depths and agent indices.
		num_agents = gameState.getNumAgents()
		max_depth = self.depth * num_agents
		#The following code follows from the psuedocode implementation on the slides but has been modified
		#Function to run alpha beta with initial a and b
		def alphaBetaSearch(gameState):
			return maxValue(gameState,0,float('-inf'),float('inf'))[1]
		
		#Function for calulcating the value of a max node also passing in a and b
		def maxValue(state,depth,a,b):
			#Getting the agent index from the depth
			agent_index = depth % num_agents
			#Return the evaluation if the node is a leaf
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state),None)

			value = -float('inf')
			action = None
			#Get the maximum of the nodes below it and return the value and action in a pair
			for act in state.getLegalActions(agent_index):
				temp = minValue(state.generateSuccessor(agent_index, act),depth+1,a,b)[0]
				if temp >= value:
					value = temp
					action = act
				#Return the value if it is greater than beta
				if value > b:
					action = act
					return (value,action)
				#Update alpha
				a = max(a,value)
			return (value, action)
		#Function for calulcating the value of a min node, same as above except for the modification for extra ghosts
		def minValue(state,depth,a,b):
			agent_index = depth % num_agents
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state),None)
			value = float('inf')
			action = None

			for act in state.getLegalActions(agent_index):
				#Check whether the next node is a max or a min and use the correct evaluation function
				if (agent_index+1)%num_agents == 0:
					temp = maxValue(state.generateSuccessor(agent_index, act),depth+1,a,b)[0]
				else:
					temp = minValue(state.generateSuccessor(agent_index, act),depth+1,a,b)[0]
				if temp <= value:
					value = temp
					action = act
				#Return the value if it is less than alpha
				if value < a:
					action = act
					return (value,action)
				#Update beta
				b = min(b,value)
			return (value, action)

		#Helper function to check terminal states
		def isTerminalState(state,depth):
			if depth >= max_depth or state.isWin() or state.isLose():
				return True
			else:
				return False

		return(alphaBetaSearch(gameState))



class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		Returns the expectimax action using self.depth and self.evaluationFunction

		All ghosts should be modeled as choosing uniformly at random from their
		legal moves.
		"""
		"*** YOUR CODE HERE ***"
		#Helper variables for checking depths and agent indices.
		num_agents = gameState.getNumAgents()
		max_depth = self.depth * num_agents
		#The following code follows from the psuedocode implementation on the slides but has been modified
		#Function to run minimax
		def expectiMax(gameState):
			return maxValue(gameState,0)[1]
		
		#Function for calulcating the value of a max node
		def maxValue(state,depth):
			#Getting the agent index from the depth
			agent_index = depth % num_agents
			#Return the evaluation if the node is a leaf
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state),None)
			value = -float('inf')
			action = None
			#Get the maximum of the nodes below it and return the value and action in a pair
			for a in state.getLegalActions(agent_index):
				temp = expValue(state.generateSuccessor(agent_index, a),depth+1)
				if  temp > value:
					value = temp
					action = a
			return (value, action)
		#Function for calulcating the expected value of a ghost node, this assumes a uniform distribution amongst moves
		#The code for managing multiple ghosts is the same
		def expValue(state,depth):
			agent_index = depth % num_agents
			if isTerminalState(state,depth):
				return (self.evaluationFunction(state))
			value = 0
			actions = state.getLegalActions(agent_index)
			for a in actions:
				#Check whether the next node is a max or a min and use the correct evaluation function
				if (agent_index+1)%num_agents == 0:
					temp = maxValue(state.generateSuccessor(agent_index, a),depth+1)[0]
				else:
					temp = expValue(state.generateSuccessor(agent_index, a),depth+1)
				value += temp/len(actions)
			return value

		#Helper function to check terminal states
		def isTerminalState(state,depth):
			if depth >= max_depth or state.isWin() or state.isLose():
				return True
			else:
				return False

		return expectiMax(gameState)
def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	#State variables to be factored into the score
	pos = currentGameState.getPacmanPosition()

	f_pos = currentGameState.getFood().asList()
	f_count= len(f_pos)
	f_dists = [util.manhattanDistance(pos, food) for food in f_pos]
	
	g_states = currentGameState.getGhostStates()
	g_scared_times = [ghostState.scaredTimer for ghostState in g_states]
	g_pos = currentGameState.getGhostPositions()
	g_dists = [util.manhattanDistance(pos, x) for x in g_pos]
	#When ghosts aren't scared, there is a large penalty for close ghosts, when they are scared, that penalty becomes a bonus
	g_score = 1
	if min(g_scared_times)>min(g_dists):
		g_score *= -1
	if min(g_dists) < 4:
		g_score *= (5-min(g_dists))**4
	#Checks wins and losses to target or avoid them
	if currentGameState.isWin():
		return 100**100
	if currentGameState.isLose():
		return -100**101

	return -f_count**10*sum(f_dists)*g_score

# Abbreviation
better = betterEvaluationFunction