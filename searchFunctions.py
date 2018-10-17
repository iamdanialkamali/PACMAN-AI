import util
import ast
from game import Directions,Actions

UNREACHABLE_GOAL_STATE = [Directions.STOP]


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def right_hand_maze_search(problem):
    """
    Q1: Search using right hand rule

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's next states:", problem.getNextStates(problem.getStartState())

    :param problem: instance of SearchProblem
    :return: list of actions
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    r = Directions.RIGHT

    x, y = problem.getStartState()  # NOW STATE

    path = []

    finish = problem.isGoalState((x, y))
    face = Directions.EAST
    right = Directions.RIGHT[face]
    left = Directions.LEFT[face]
    reverse = Directions.REVERSE[face]


    while (finish == False):
        #input()
        print problem.goal
        print x, y
        reverseIsOpen = False
        forwardIsOpen = False
        leftIsOpen = False
        rightIsOpen = False
        nextStates = problem.getNextStates((x, y))

        if len(nextStates) > 0:
            for node in nextStates:
                if (node[1] == right):
                    rightIsOpen = True
                    rightWay = [node[0], right]
                if (node[1] == face):
                    forwardIsOpen = True
                    forwardWay = [node[0], face]
                if (node[1] == left):
                    leftIsOpen = True
                    leftWay = [node[0], left]
                if (node[1] == reverse):
                    reverseIsOpen = True
                    reverseWay = [node[0], reverse]

            if rightIsOpen:
                x, y = rightWay[0]  # New Location
                face = rightWay[1]  # New Face to
                path.append(face)
            elif forwardIsOpen:
                x, y = forwardWay[0]  # New Location
                face = forwardWay[1]  # New Face to
                path.append(face)
            elif leftIsOpen:
                x, y = leftWay[0]  # New Location
                face = leftWay[1]  # New Face to
                path.append(face)
            elif reverseIsOpen:
                x, y = reverseWay[0]  # New Location
                face = reverseWay[1]  # New Face to
                path.append(face)

            else:
                path.append(Directions.STOP)

            right = Directions.RIGHT[face]
            left = Directions.LEFT[face]
            reverse = Directions.REVERSE[face]

        else:
            path.append(Directions.STOP)

        finish = problem.isGoalState((x, y))

    path.append(Directions.STOP)

    return path

def dfs(problem):
    """
    Q2: Search the deepest nodes in the search tree first.
    """

    "*** YOUR CODE HERE ***"


    x, y = problem.getStartState()  # NOW STATE
    startPoint = problem.getStartState()
    path = []

    finish = problem.isGoalState((x, y))

    parent = {}
    stack = util.Stack()
    while (finish == False):

        nextStates = problem.getNextStates((x, y))


        for node in nextStates:
            if(parent.keys().__contains__(str(node[0]))==False):
                parent[str(node[0])] = str((x, y))+'/'+node[1]
                stack.push(node[0])
        x,y = stack.pop()
        finish = problem.isGoalState((x, y))
    state = str(problem.goal)

    while state != str(startPoint):
        data = parent[state].split('/')
        state = data[0]
        path.append(data[1])
    path.reverse()
    print ('DONE')
    return path



def bfs(problem):
    """
    Q3: Search the shallowest nodes in the search tree first.
    """

    "*** YOUR CODE HERE ***"

    myState = problem.getStartState()  # NOW STATE
    startPoint = myState[:]


    finish = problem.isGoalState(myState)
    parents = {}
    queue = util.Queue()
    queue.push(startPoint)
    while (finish == False ):

        myState = queue.pop()
        print myState
        nextStates = problem.getNextStates(myState)
        # print nextStates
        # input()
        for node in nextStates:
            if (parents.has_key(node[0]) == False):
                parents[node[0]] = myState
                queue.push(node[0])

        finish = problem.isGoalState(myState)

    input()
    path = getPath(parents, startPoint[:], myState[:])

    return path
def ucs(problem):
    """
    Q6: Search the node of least total cost first.
    """
    x, y = problem.getStartState()  # NOW STATE
    startPoint = problem.getStartState()

    parents = {}
    path = []
    queue = util.PriorityQueue()
    parents[str((x, y))] = str((x, y)) + '/' + 'NOTHING' + '/' + str(0)
    queue.push([(x, y),0],0)
    while (queue.isEmpty()==False):
        (x,y),cost = queue.pop()

        nextStates = problem.getNextStates((x, y))

        for node in nextStates:
            if node[0]!=startPoint:
                nodeCost = cost+node[2]
                if(parents.keys().__contains__(str(node[0]))==True):

                    prevData = parents[str(node[0])].split('/')

                    if(int(prevData[2]) > nodeCost):

                        parents[str(node[0])] =str((x, y))+'/' + node[1] +'/'+str(nodeCost)
                        queue.push([node[0], nodeCost], nodeCost)

                else:
                    parents[str(node[0])] = str((x, y)) + '/' + node[1] + '/' + str(nodeCost)
                    queue.push([node[0], nodeCost], nodeCost)

    path = get_path(parents, startPoint, problem.goal)
    return path



def getPath(parent, startState, goal):
    result = []
    state = goal

    while (state != startState):
        childx, childy = state[0] , state[1]
        state = parent[state]
        parentx, parenty = state[0] , state[1]
        action = Actions.vectorToDirection((childx - parentx, childy - parenty))
        result.insert(0, action)
    return result

def get_path(parents , startPoint,finalPoint):
    state = str(finalPoint)
    startPoint = str(startPoint)
    path = []
    while(state != startPoint):
        state = parents[state].split('/')
        path.insert(0,state[1])
        state = state[0]
        print state
    return path
