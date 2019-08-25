# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily creaed by John DeNero
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

        "*** YOUR CODE HERE ***"


        #avoid ghosts without having a power pellet
        #catch ghosts when having a power pellet
        distanceGhost = 2147483648
        score = successorGameState.getScore()
        #nearest ghost
        for i in newGhostStates:
            if manhattanDistance(newPos,i.getPosition()) < distanceGhost:
                distanceGhost = manhattanDistance(newPos,i.getPosition())

        remainScaredTime = 0
        for  i in newScaredTimes:
            remainScaredTime+=i

        if remainScaredTime>0:
            if distanceGhost != 0:
                score += 30/distanceGhost
        else:
            if distanceGhost != 0:
                score -= 2/distanceGhost

        #nearest food
        distanceFood = 2147483648
        for f in newFood.asList():
            if distanceFood > manhattanDistance(newPos,f):
                distanceFood = manhattanDistance(newPos,f)

        if distanceFood != 0:
            score += 1.5/distanceFood

        return score



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
        """
        "*** YOUR CODE HERE ***"
    def getAction(self, gameState):

        def compute_minimax(gameState, num, index ,depth):

            #Pacman wants to get maximum
            if index == 0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:  return self.evaluationFunction(gameState)
                maxTemp = -2147483648
                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(0, action)
                    temp = compute_minimax(afterStates,num,1,depth)
                    if temp > maxTemp: maxTemp = temp

                return maxTemp

            #Ghosts want to get minimum
            if index>0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:  return self.evaluationFunction(gameState)
                minTemp = 2147483648
                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(index, action)

                    if index < num-1:
                        temp = compute_minimax(afterStates,num,index+1,depth)
                    else: #All ghost have moved in depth. Now, pacman turn.
                        temp = compute_minimax(afterStates,num,0,depth+1)
                    if temp < minTemp: minTemp = temp

                return minTemp

        #compute from pacman with index 0
        #because we want to get the action we need to write it separately..
        maxTemp = -2147483648
        move = []
        for action in gameState.getLegalActions(0):
            afterStates =  gameState.generateSuccessor(0, action)
            temp = compute_minimax(afterStates,gameState.getNumAgents(),1,0)
            if temp > maxTemp:
                maxTemp = temp
                move = action

        return move



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def compute_minimax(gameState, num, index, depth, alpha, beta):

            #Pacman wants to get maximum
            if index == 0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:
                    return self.evaluationFunction(gameState)

                maxTemp = -2147483648
                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(0, action)
                    temp = compute_minimax(afterStates,num,1,depth,alpha,beta)
                    if temp > maxTemp: maxTemp = temp
                    #Pruning
                    if maxTemp > beta: return maxTemp
                    alpha = max(alpha,maxTemp)

                return maxTemp

            #Ghosts want to get minimum
            if index>0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:
                     return self.evaluationFunction(gameState)

                minTemp = 2147483648
                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(index, action)

                    if index < num-1:
                        temp = compute_minimax(afterStates,num,index+1,depth,alpha,beta)
                    else: #All ghost have moved in depth. Now, pacman turn.
                        temp = compute_minimax(afterStates,num,0,depth+1,alpha,beta)

                    if temp < minTemp: minTemp = temp

                    #Pruning
                    if minTemp < alpha: return minTemp
                    beta = min(beta,minTemp)

                return minTemp

        #compute from pacman with index 0
        #because we want to get the action we need to write it separately..
        maxTemp = -2147483648
        alpha = -2147483648
        beta = 2147483648
        move = []

        for action in gameState.getLegalActions(0):
            afterStates =  gameState.generateSuccessor(0, action)
            temp = compute_minimax(afterStates,gameState.getNumAgents(),1,0,alpha,beta)
            if temp > maxTemp:
                maxTemp = temp
                move = action
                if temp>alpha: alpha=temp

        return move

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
        def compute_minimax(gameState, num, index ,depth):

            #Pacman wants to get maximum
            if index == 0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:  return self.evaluationFunction(gameState)
                maxTemp = -2147483648
                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(0, action)
                    temp = compute_minimax(afterStates,num,1,depth)
                    if temp > maxTemp: maxTemp = temp

                return maxTemp

            #Ghosts want to get minimum
            if index>0:
                if  gameState.isWin() or gameState.isLose() or depth == self.depth:  return self.evaluationFunction(gameState)
                minTemp = 2147483648

                sumScore=0;
                sumAction=0;

                for action in gameState.getLegalActions(index):
                    afterStates =  gameState.generateSuccessor(index, action)

                    if index < num-1:
                        temp = compute_minimax(afterStates,num,index+1,depth)
                    else: #All ghost have moved in depth. Now, pacman turn.
                        temp = compute_minimax(afterStates,num,0,depth+1)
                    sumScore+=temp;
                    sumAction+=1;

                return sumScore/sumAction

        #compute from pacman with index 0
        #because we want to get the action we need to write it separately..
        maxTemp = -2147483648
        move = []
        for action in gameState.getLegalActions(0):
            afterStates =  gameState.generateSuccessor(0, action)
            temp = compute_minimax(afterStates,gameState.getNumAgents(),1,0)
            if temp > maxTemp:
                maxTemp = temp
                move = action

        return move

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    distanceGhost = 2147483648
    score = currentGameState.getScore()
    #nearest ghost
    for i in newGhostStates:
        if manhattanDistance(newPos,i.getPosition()) < distanceGhost:
            distanceGhost = manhattanDistance(newPos,i.getPosition())

    remainScaredTime = 0
    for  i in newScaredTimes:
        remainScaredTime+=i

    #catching ghost get large reward
    if remainScaredTime>0:
        if distanceGhost <= remainScaredTime and distanceGhost != 0:
            score += 30/distanceGhost
    else:
        if distanceGhost != 0:
            score -= 2/distanceGhost

    #nearest food
    distanceFood = 2147483648
    for f in newFood.asList():
        if distanceFood > manhattanDistance(newPos,f):
            distanceFood = manhattanDistance(newPos,f)

    if distanceFood != 0:
        score += 1.7/distanceFood

    #farest food
    distanceFood = -1
    for f in newFood.asList():
        if distanceFood < manhattanDistance(newPos,f):
            distanceFood = manhattanDistance(newPos,f)

    if distanceFood != 0:
        score -= 0.2/distanceFood

    return score


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
