# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        for ghostState in newGhostStates:
          if util.manhattanDistance(newPos, ghostState.getPosition()) <= 1:
            return -99999999

        countFood = newFood.count(True)
        if countFood == 0:
          return 99999999

        walls = successorGameState.getWalls()
        foods = successorGameState.getFood()
        pacPos = successorGameState.getPacmanPosition()

        def getLegalNextPosition(walls, pos):
          posx = pos[0]
          posy = pos[1]
          nextPositions = []
          for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            if walls[posx+dx][posy+dy] == False:
              nextPositions.append((posx+dx,posy+dy))
          return nextPositions

        frontier = util.Queue()
        explored = []

        node = {'state':pacPos, 'cost':0}
        frontier.push(node)

        while not frontier.isEmpty():
          thisNode = frontier.pop()  
          if thisNode['state'] in explored:
            continue
          xx, yy = thisNode['state']
          if foods[xx][yy]:
            nearestFoodDistance = thisNode['cost']
            break
          explored.append(thisNode['state'])
          nextPositions = getLegalNextPosition(walls, thisNode['state'])
          for nextPosition in nextPositions:
            node = {'state':nextPosition, 'cost':thisNode['cost']+1}
            frontier.push(node)
        pass

        """
        nearestFoodDistance = 1000
        for x, items in enumerate(newFood):
          for y, item in enumerate(items):
            if newFood[x][y] == True:
              #print (x,y), newPos
              if util.manhattanDistance(newPos, (x,y)) < nearestFoodDistance:
                nearestFoodDistance = util.manhattanDistance(newPos, (x,y))
        #print currentGameState.getPacmanPosition(), nearestFoodDistance
        """
        return 1000 - nearestFoodDistance - countFood*100

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
    def max_choice(self, gameState, depth):
      #return (value, this_node_action)
      actions = gameState.getLegalActions(0)
      max_temp = -99999999
      action_temp = None
      for action in actions:
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(0, action), depth=depth+1)
        if this_value > max_temp:
          max_temp = this_value
          action_temp = action
      return (max_temp, action_temp)

    def min_choice(self, gameState, depth):
      #return (value, this_node_action)
      agentIndex = depth % gameState.getNumAgents()
      actions = gameState.getLegalActions(agentIndex)
      min_temp = 99999999
      action_temp = None
      for action in actions:
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(agentIndex, action), depth=depth+1)
        if this_value < min_temp:
          min_temp = this_value
          action_temp = action
      return (min_temp, action_temp)

    def gameOver(self, gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
        return True
      else:
        return False

    def this_node_choice(self, gameState, depth):
      #return (value, this_node_action)
      if self.gameOver(gameState, depth):
        return (self.evaluationFunction(gameState), None)
      if depth % gameState.getNumAgents() == 0:
        return self.max_choice(gameState, depth)
      else:
        return self.min_choice(gameState, depth)
    
    def getAction(self, gameState): 
        """
          gameState --> multiagentTestClasses.MultiagentTreeState
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
        """
        "*** YOUR CODE HERE ***"
        root_max_value, root_max_action = self.this_node_choice(gameState, 0)
        return root_max_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def max_choice(self, gameState, depth, alpha, beta):
      #return (value, this_node_action)
      actions = gameState.getLegalActions(0)
      max_temp = -99999999
      action_temp = None
      for action in actions:
        #prune
        if max_temp > beta:
          continue
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(0, action), 
          depth=depth+1, alpha=max(max_temp, alpha), beta=beta)
        if this_value > max_temp:
          max_temp = this_value
          action_temp = action
      return (max_temp, action_temp)

    def min_choice(self, gameState, depth, alpha, beta):
      #return (value, this_node_action)
      agentIndex = depth % gameState.getNumAgents()
      actions = gameState.getLegalActions(agentIndex)
      min_temp = 99999999
      action_temp = None
      for action in actions:
        #prune
        if min_temp < alpha:
          continue
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(agentIndex, action), 
          depth=depth+1, alpha=alpha, beta=min(min_temp, beta))
        if this_value < min_temp:
          min_temp = this_value
          action_temp = action
      return (min_temp, action_temp)

    def gameOver(self, gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
        return True
      else:
        return False

    def this_node_choice(self, gameState, depth, alpha, beta):
      #return (value, this_node_action)
      if self.gameOver(gameState, depth):
        return (self.evaluationFunction(gameState), None)
      if depth % gameState.getNumAgents() == 0:
        return self.max_choice(gameState, depth, alpha = alpha, beta = beta)
      else:
        return self.min_choice(gameState, depth, alpha = alpha, beta = beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root_max_value, root_max_action = self.this_node_choice(gameState, depth = 0, alpha = -99999999, beta = 99999999)
        return root_max_action
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def max_choice(self, gameState, depth):
      #return (value, this_node_action)
      actions = gameState.getLegalActions(0)
      max_temp = -99999999
      action_temp = None
      for action in actions:
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(0, action), depth=depth+1)
        if this_value > max_temp:
          max_temp = this_value
          action_temp = action
      return (max_temp, action_temp)

    def expect_choice(self, gameState, depth):
      #return (value, this_node_action)
      agentIndex = depth % gameState.getNumAgents()
      actions = gameState.getLegalActions(agentIndex)
      min_temp = 99999999
      action_temp = None
      sum_value = 0
      for action in actions:
        this_value, suc_action = self.this_node_choice(gameState=gameState.generateSuccessor(agentIndex, action), depth=depth+1)
        sum_value += this_value
      return (float(sum_value)/float(len(actions)), action_temp)

    def gameOver(self, gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
        return True
      else:
        return False

    def this_node_choice(self, gameState, depth):
      #return (value, this_node_action)
      if self.gameOver(gameState, depth):
        return (self.evaluationFunction(gameState), None)
      if depth % gameState.getNumAgents() == 0:
        return self.max_choice(gameState, depth)
      else:
        return self.expect_choice(gameState, depth)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        root_max_value, root_max_action = self.this_node_choice(gameState, 0)
        return root_max_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

