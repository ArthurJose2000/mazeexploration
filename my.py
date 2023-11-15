from pyamaze import maze,agent,COLOR
import sys
import random
import csv
import statistics

class MyAlgorithm:
    def __init__(self, maze, numOfAgents, colorList, start=None):
        self.maze = maze
        self.numOfAgents = numOfAgents
        self.colorList = colorList
        self.start = start
        self.compass = "NESW" # it establishes the children's storage order
        self.filledInterval = [False for i in range(numOfAgents)]

        # Test
        self.filledInterval2 = [False for i in range(numOfAgents)]

        # Test
        self.modified = [False for i in range(numOfAgents)]

        # Test
        self.currentAgentInterval = (0, 1)

        if self.start is None:
            self.start = (self.maze.rows,self.maze.cols)

    # Run the algorithm
    def run(self):
        """ print("MY ALGORITHM - TRABALHO DE GRADUAÇÃO")
        print("QUANTIDADE DE AGENTES: ", self.numOfAgents)
        print() """

        division = 1.0 / self.numOfAgents
        paths = []
        explored = []
        agents_search = []
        pionner_steps = sys.maxsize
        totalSteps = 0

        #strange steps
        pioneer_after_interval1 = 0
        pioneer_after_interval2 = 0
        steps_agents_using_interval2 = 0

        for i in range(0, self.numOfAgents):
            start = i * division
            end = (i + 1) * division

            # Test            
            #agentInterval = (start, end)
            self.currentAgentInterval = (start, end)

            agentColor = self.colorList[i % len(self.colorList)]

            # Test
            #mySearch, effective_path, explored_cells, foundTheGoal = self.run_single_agent(agentInterval, i)
            mySearch, effective_path, explored_cells, foundTheGoal, steps_after_interval1, steps_after_interval2 = self.run_single_agent(i)

            if steps_after_interval1 != 0 and steps_after_interval2 == 0:
                steps_agents_using_interval2 += steps_after_interval1

            #print("steps_after_interval1: ", steps_after_interval1)
            #print("steps_after_interval2: ", steps_after_interval2)

            self.concatenate_new_elements(explored, explored_cells)

            """ print("AGENTE ", i + 1)
            print("Cor: ", self.getColorString(agentColor))
            print("Intervalo: ", self.getIntervalString(agentInterval))
            print("Caminho eficaz pela árvore (representação mixed radix): ", self.getMixedRadixRepresentation(effective_path, self.maze))
            print() """

            a = agent(self.maze,footprints=True,color=agentColor,shape='square',filled=True)

            paths.append({a:mySearch})
            agents_search.append(mySearch)

            # Number of steps of the agent. Subtract 1 to consider that the first cell is not countable
            agent_steps = len(mySearch) - 1

            # Count the total number of steps
            totalSteps += agent_steps

            # Get the number of the steps of the pionner
            if foundTheGoal == True:
                if pionner_steps > agent_steps:
                    pionner_steps = agent_steps
                    pioneer_after_interval1 = steps_after_interval1
                    pioneer_after_interval2 = steps_after_interval2

        if pionner_steps == sys.maxsize:
            print("ERRO")

        # Get the explored fraction of the maze
        fraction = len(explored) / (self.maze.rows * self.maze.cols)

        # Calculate the fraction of the maze explored until the pionner find the goal
        cells = []
        for i in range(self.numOfAgents):
            aux = agents_search[i][0:pionner_steps]

            for e in aux:
                if e not in cells:
                    cells.append(e)
        fraction_pionner = len(cells) / (self.maze.rows * self.maze.cols)


        # Show only agent i
        # self.maze.tracePaths([paths[2]], kill=False, delay=100)

        """ #self.maze.tracePaths(paths, kill=False, delay=100)
        self.maze.tracePaths_by_key_press(paths, kill=False)

        self.maze.run() """

        #print("pioneer_after_interval1: ", pioneer_after_interval1)
        #print("pioneer_after_interval2: ", pioneer_after_interval2)

        return totalSteps, pionner_steps, fraction, fraction_pionner, pioneer_after_interval1, pioneer_after_interval2, steps_agents_using_interval2

    # Run the algorithm for a single agent
    def run_single_agent(self, agentIndex):
        explored = [self.start]
        mySearch = []

        parentList = []
        parentList.append((-1,-1))
        currCell = self.start
        agent_path = []
        effective_path = []

        # Some agents will not find the goal because
        # currently the algorithm has a stop condition
        foundTheGoal = False


        steps_after_interval1 = 0
        steps_after_interval2 = 0

        while True:

            if self.filledInterval[agentIndex] == True:
                steps_after_interval1 += 1

            if self.filledInterval2[agentIndex] == True:
                steps_after_interval2 += 1

            if currCell==self.maze._goal:
                mySearch.append(currCell)
                effective_path.append(currCell)
                foundTheGoal = True
                break

            # If there are not non-visited children, go to parent
            nonVisitedChildren, allChildren = self.getChildrenPoints(currCell, self.maze.maze_map[currCell], parentList[-1], explored)
            count_nonVisitedChildren = len(nonVisitedChildren)
            if count_nonVisitedChildren == 0:
                if currCell not in explored:
                    explored.append(currCell)

                mySearch.append(currCell)

                # Stop condition
                if currCell == self.start:
                    break
                
                currCell = parentList.pop()
                effective_path.pop()
                agent_path.pop()

                continue

            # Define the next step to the agent
            # If next == -1, go to parent

            # Test
            #next = self.defineAgentNextStep(agentInterval, agent_path, allChildren, nonVisitedChildren, currCell, agentIndex)
            next = self.defineAgentNextStep( agent_path, allChildren, nonVisitedChildren, currCell, agentIndex)

            if next == -1:
                if currCell not in explored:
                    explored.append(currCell)

                mySearch.append(currCell)

                if currCell != self.start:
                    currCell = parentList.pop()
                    effective_path.pop()
                    agent_path.pop()

                continue
            
            childCellPoint = allChildren[next]

            if currCell not in explored:
                explored.append(currCell)

            parentList.append(currCell)
            mySearch.append(currCell)
            effective_path.append(currCell)
            if childCellPoint=='N':
                currCell = (currCell[0]-1,currCell[1])
            elif childCellPoint=='E':
                currCell = (currCell[0],currCell[1]+1)
            elif childCellPoint=='S':
                currCell = (currCell[0]+1,currCell[1])     
            elif childCellPoint=='W':
                currCell = (currCell[0],currCell[1]-1)

        return mySearch, effective_path, explored, foundTheGoal, steps_after_interval1, steps_after_interval2

    # Return children's cardinal points in preferential order 
    def getChildrenPoints(self, cellCoordinate, cellPoints, parent, explored):
        allChildren = []
        nonVisitedChildren = []
        for d in self.compass:
            if cellPoints[d] == True:
                if d=='N':
                    childCell = (cellCoordinate[0]-1,cellCoordinate[1])
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('N')
                        continue

                    allChildren.append('N')
                    nonVisitedChildren.append('N')
                elif d=='E':
                    childCell = (cellCoordinate[0],cellCoordinate[1]+1)
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('E')
                        continue

                    allChildren.append('E')
                    nonVisitedChildren.append('E')
                elif d=='S':
                    childCell = (cellCoordinate[0]+1,cellCoordinate[1])
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('S')
                        continue

                    allChildren.append('S')
                    nonVisitedChildren.append('S')
                elif d=='W':
                    childCell = (cellCoordinate[0],cellCoordinate[1]-1)
                    if parent == childCell:
                        continue
                    if childCell in explored:
                        allChildren.append('W')
                        continue

                    allChildren.append('W')
                    nonVisitedChildren.append('W')

        return nonVisitedChildren, allChildren

    # If there is child to visit, this function will decide what child to visit
    # This function doesn't work if there is no child to visit
    def defineAgentNextStep(self, agent_path, allChildren, nonVisitedChildren, currCell, agentIndex):

        totalNumberOfChildren = len(allChildren)
        
        # If there is only 1 child just go on
        if totalNumberOfChildren == 1:
            agent_path.append((-1, -1))
            return 0
        
        # Get the weight interval of each node
        relative_node_weights = self.getRelativeNodeWeights(agent_path, totalNumberOfChildren)
        """ print("agentInterval: ", self.currentAgentInterval)
        print("relative_node_weights: ", relative_node_weights)
        print("agent_path: ", agent_path)
        print("totalNumberOfChildren: ", totalNumberOfChildren) """

        # MELHORAR ESTE PASSO A PASSO
        # Following steps if there is more than 1 child and if the agent has not finished its interval:
        # - If the agent finds a child that intersects the agent's interval, it goes to this node if the agent didn't visit the node
        # - If the agent finds a child that intersects the agent's interval but this node was visited, the agent will check the next
        # child, coming back to the first step
        # - If the agent find a child that doesn't intersect the agent's interval, there is two possibilities:
        #     - if the child's interval is on the left of the agent's interval, it will check the next child, coming
        #     back to the first step
        #     - if the child's interval is on the right of the agent's interval, surely the agent finished its interval,
        #     and it will do a dummy DFS
        # - If no child fills the agent's requirement, the agent will go to the parent

        if self.filledInterval[agentIndex] == False:
            # Return the first child that is able to obey the limits
            for i in range(0, totalNumberOfChildren):

                # If the current child's interval is on the right of the agent's interval, surely the agent finished its interval
                if self.currentAgentInterval[1] <= relative_node_weights[i][0]:
                    self.filledInterval[agentIndex] = True
                    break

                # nodeIsInsideAgentInterval = self.currentAgentInterval[0] < relative_node_weights[i][1]
                nodeIsInsideAgentInterval = self.currentAgentInterval[0] < relative_node_weights[i][1] and self.currentAgentInterval[1] > relative_node_weights[i][0]
                nodeWasNotVisistedByTheAgent = allChildren[i] in nonVisitedChildren

                if nodeIsInsideAgentInterval and nodeWasNotVisistedByTheAgent:
                    agent_path.append((i, totalNumberOfChildren))
                    return i

            # If the agent is in the root and it doesn't find a node that fills the requirement, it finished its interval
            if currCell == self.start:
                self.filledInterval[agentIndex] = True

            # If the agent doesn't finish its interval and no node that fills the requirement was found, it goes to parent
            if self.filledInterval[agentIndex] == False:
                return -1
            
        # Rising until find the limit of the second interval
        if self.filledInterval[agentIndex] == True and self.modified[agentIndex] == False:

            chunk = self.currentAgentInterval[1] - self.currentAgentInterval[0]
            newInterval = (0, 0)

            if self.currentAgentInterval[1] == 1:
                newInterval = (0, chunk)
            else:
                newInterval = (self.currentAgentInterval[1], self.currentAgentInterval[1] + chunk)

            
            if self.currentAgentInterval[1] == 1 and currCell != self.start:
                return -1

            for i in range(0, totalNumberOfChildren):

                if newInterval[1] <= relative_node_weights[i][1]:

                    self.modified[agentIndex] = True
                    self.currentAgentInterval = newInterval

                    # Must not happen
                    if newInterval[1] < relative_node_weights[i][0]:
                        print("ERRO")

                    break

            if self.modified[agentIndex] == False:
                return -1

        if self.filledInterval2[agentIndex] == False:

            # Return the first child that is able to obey the limits
            for i in range(0, totalNumberOfChildren):

                index = totalNumberOfChildren - i - 1

                # If the current child's interval is on the left of the agent's interval, surely the agent finished its interval
                if self.currentAgentInterval[0] >= relative_node_weights[index][1]:
                    self.filledInterval2[agentIndex] = True
                    break

                # nodeIsInsideAgentInterval = self.currentAgentInterval[0] < relative_node_weights[i][1]
                nodeIsInsideAgentInterval = self.currentAgentInterval[0] < relative_node_weights[index][1] and self.currentAgentInterval[1] > relative_node_weights[index][0]
                nodeWasNotVisistedByTheAgent = allChildren[index] in nonVisitedChildren
                if nodeIsInsideAgentInterval and nodeWasNotVisistedByTheAgent:
                    agent_path.append((index, totalNumberOfChildren))
                    return index

            # If the agent is in the root and it doesn't find a node that fills the requirement, it finished its interval
            if currCell == self.start:
                self.filledInterval2[agentIndex] = True

            # If the agent doesn't finish its interval and no node that fills the requirement was found, it goes to parent
            if self.filledInterval2[agentIndex] == False:
                return -1


        # The agent surely finished its interval, and it will do a dummy 
        for i in range(0, totalNumberOfChildren):
            if allChildren[i] in nonVisitedChildren:
                agent_path.append((i, totalNumberOfChildren))
                return i

    def getRelativeNodeWeights(self, agent_path, count_children):

        # Calculating the previous node interval according the agent path
        # It is the way that we can calculate values related to a number less than 1 in a mixed radix
        path_size = len(agent_path)
        node_interval = (0, 1)
        if path_size > 0:
            if agent_path[0][0] != -1: # only if the first related node has more than one child
                chunk = 1 / agent_path[0][1]
                node_interval = (agent_path[0][0] * chunk,  agent_path[0][0] * chunk + chunk)

            for i in range(1, path_size):
                if agent_path[i][0] == -1:
                    continue

                node_interval_size = node_interval[1] - node_interval[0]
                chunk = node_interval_size / agent_path[i][1]
                node_interval = (node_interval[0] + agent_path[i][0] * chunk, node_interval[0] + agent_path[i][0] * chunk + chunk)

        # Calculating the weights of the next nodes
        weights = []
        node_interval_size = node_interval[1] - node_interval[0]
        chunk = node_interval_size / count_children
        start = 0
        end = 0
        for i in range(0, count_children):
            start = node_interval[0] + chunk * i
            end = start + chunk
            weight = (start, end)
            weights.append(weight)

        return weights

    # Auxiliary function to print agent color
    def getColorString(self, color):
        if color == COLOR.red:
            return "Vermelho"
        elif color == COLOR.blue:
            return "Azul"
        elif color == COLOR.yellow:
            return "Amarelo"
        elif color == COLOR.cyan:
            return "Ciano"
        elif color == COLOR.black:
            return "Preto"
        elif color == COLOR.pink:
            return "Rosa"
        elif color == COLOR.orange:
            return "Laranja"

    # Auxiliary function to print agent interval
    def getIntervalString(self, interval):
        if interval[1] > 0.9999:
            return "[" + str(interval[0]) + ", 1]"
        else:
            return "[" + str(interval[0]) + ", " + str(interval[1]) + "["
        
    # Auxiliary function to print the next direction
    def next_direction(self, current, next):
        if current[0] != next[0]:
            if current[0] < next[0]:
                return "S"
            else:
                return "N"
        else:
            if current[1] < next[1]:
                return "E"
            else:
                return "W"

    # Auxiliary function to get the mixed radix representation of the agent effective_path
    def getMixedRadixRepresentation(self, effective_path, maze):
        mixedRadix = [(0, 0)]
        
        for i in range(0, len(effective_path) - 1):
            radix = 0
            next = self.next_direction(effective_path[i], effective_path[i + 1])

            directions = []
            if maze.maze_map[effective_path[i]]['N'] == 1 and (effective_path[i][0] - 1, effective_path[i][1]) != effective_path[i - 1]:
                radix += 1
                directions.append('N')
            if maze.maze_map[effective_path[i]]['E'] == 1 and (effective_path[i][0], effective_path[i][1] + 1) != effective_path[i - 1]:
                radix += 1
                directions.append('E')
            if maze.maze_map[effective_path[i]]['S'] == 1 and (effective_path[i][0] + 1, effective_path[i][1]) != effective_path[i - 1]:
                radix += 1
                directions.append('S')
            if maze.maze_map[effective_path[i]]['W'] == 1 and (effective_path[i][0], effective_path[i][1] - 1) != effective_path[i - 1]:
                radix += 1
                directions.append('W')

            digit = directions.index(next)

            if radix == 1:
                radix = "X"
                digit = "X"

            mixedRadix.append((digit, radix))

        return mixedRadix
    
    # Auxiliary function to concatenate to add only new elements to array
    def concatenate_new_elements(self, main, vector):
        for e in vector:
            if e not in main:
                main.append(e)
    

class TarryGeneralization:
    def __init__(self, maze, numOfAgents, colorList, start=None):
        self.maze = maze
        self.numOfAgents = numOfAgents
        self.colorList = colorList
        self.start = start

        if self.start is None:
            self.start = (self.maze.rows,self.maze.cols)

    # Run the algorithm
    def run(self):
        """ print("GENERALIZATION OF TARRY'S ALGORITHM")
        print("QUANTIDADE DE AGENTES: ", self.numOfAgents)
        print() """

        paths = []
        agents_search, fraction = self.run_agents()
        pionner_steps = sys.maxsize
        last_steps = 0
        totalSteps = 0

        for i in range(0, len(agents_search)):
            agentColor = self.colorList[i % len(self.colorList)]
            a = agent(self.maze,footprints=True,color=agentColor,shape='square',filled=True)
            paths.append({a:agents_search[i]})

            # Number of steps of the agent. Subtract 1 to consider that the first cell is not countable
            agent_steps = len(agents_search[i]) - 1

            # Count the total number of steps
            totalSteps += agent_steps

            # Get the number of the steps of the pionner
            pionner_steps = agent_steps if pionner_steps > agent_steps else pionner_steps

            # Get the number of the steps of the last agent that found the goal
            last_steps = agent_steps if last_steps < agent_steps else last_steps


        # Show only agent i
        # self.maze.tracePaths([paths[2]], kill=False, delay=100)

        """ #self.maze.tracePaths(paths, kill=False, delay=50)
        self.maze.tracePaths_by_key_press(paths, kill=False)

        self.maze.run() """

        return totalSteps, pionner_steps, fraction, last_steps

    # Run the algorithm for all agents
    # The following steps come from the article "Multi-Agent Maze Exploration" - Kivelevitch and Cohen 2010
    def run_agents(self):

        # Matrix of the search of each agent
        agents_search = []

        # Matrix of the effective of each agent
        # It will be trully computed only in the PHASE 1 of the algorithm
        # In PHASE 2 it is useful only to know the effective path of the pionner agent
        effective_path = []

        # Matrix of the explored cells by each agent 
        agents_exploredCells = []

        # Array of the current cell of each agent
        agents_currentCell = []

        # Matrix of the parents list of each agent
        agents_parents = []

        # Array of the explored cells
        exploredCells = []
        exploredCells.append(self.start)

        # Array of dead-end cells
        deadEndCells = []

        # Array of booleans that indicates if an agent found the goal
        foundTheGoal = []

        # Matrix of the Last Common Location (LCL) of each agent related to the others
        lcl = []


        for i in range(0, self.numOfAgents):
            agents_search.append([self.start])
            effective_path.append([self.start])
            agents_exploredCells.append([self.start])
            agents_currentCell.append(self.start)
            agents_parents.append([(-1,-1)])
            foundTheGoal.append(False)
            lcl.append([])

            for j in range(0, self.numOfAgents):
                lcl[i].append(self.start)

        
        # Pay attention: this algorithm is divided in two phases. In the first phase, the agents
        # follow 6 steps until some agent finds the goal. If some agent finds the goal, the second
        # phase will start. In the second phase, the agents that doesn't find the goal, will go to
        # the Last Common Location (LCL) with the pionner agent, and then the agents will follow the
        # goal path

        # PHASE 1
        while True not in foundTheGoal:

            # During each loop all the agents follow the steps below
            # Step 1: The agent should move to cells that have not been traveled by any agent
            # Step 2: If there are several such cells, the agent should choose one arbitrarily
            # Step 3: If there is no cell that has not been traveled by an agent, the agent should prefer to move to a cell that has not been traveled by it
            # Step 4: If all the possible directions have already been traveled by the agent, or if the agent has reached a dead-end, the agent should retreat until a cell that meets one of the previous conditions
            # Step 5: All the steps should be logged by the agent in its history
            # Step 6: When retreating, mark the cells retreated from as “dead end”
            for i in range(0, self.numOfAgents):

                # If the agent found the goal, go to the next agent
                if foundTheGoal[i] == True:
                    continue

                # Get cell children
                currentCell = agents_currentCell[i]
                parent = agents_parents[i][-1]
                children = self.getChildren(currentCell, self.maze.maze_map[currentCell], parent)

                # Check cell children
                visited = []
                nonVisited = []
                for child in children:
                    if child not in deadEndCells:
                        if child in exploredCells:
                            visited.append(child)
                        else:
                            nonVisited.append(child)

                # If there is non visited cells, choose one arbitrarily
                if len(nonVisited) > 0:
                    # Update parents list
                    agents_parents[i].append(agents_currentCell[i])

                    # Go to child
                    agents_currentCell[i] = nonVisited[random.randint(0, len(nonVisited) - 1)]

                    # Update the general array of explored cells
                    if agents_currentCell[i] not in exploredCells:
                        exploredCells.append(agents_currentCell[i])

                    # Update the array of the explored cells by the agent
                    if agents_currentCell[i] not in agents_exploredCells[i]:
                        agents_exploredCells[i].append(agents_currentCell[i])

                    # Update agent's effective path
                    effective_path[i].append(agents_currentCell[i])

                # If there is no cell that has not been visted by an agent, the agent should prefer to move to a cell that has not been visted by it
                elif len(visited) > 0:
                    agent_nonVisited = []

                    for child in visited:
                        if child not in agents_exploredCells[i]:
                            agent_nonVisited.append(child)

                    # Update parents list
                    agents_parents[i].append(agents_currentCell[i])

                    # Go to child
                    agents_currentCell[i] = agent_nonVisited[random.randint(0, len(agent_nonVisited) - 1)]

                    # Update the array of the explored cells by the agent
                    agents_exploredCells[i].append(agents_currentCell[i])

                    # Update agent's effective path
                    effective_path[i].append(agents_currentCell[i])


                # No children - dead-end
                else:
                    deadEndCells.append(agents_currentCell[i])

                    # Go to parent
                    agents_currentCell[i] = agents_parents[i].pop()
                    effective_path[i].pop()

                # Update agent search path
                agents_search[i].append(agents_currentCell[i])

                # Update the Last Common Location (LCL) matrix if it is necessary
                for j in range(0, self.numOfAgents):
                    if i == j:
                        continue

                    if agents_currentCell[i] in effective_path[j]:
                        lcl[i][j] = agents_currentCell[i]
                        lcl[j][i] = agents_currentCell[i]

                # Check if the agent found the goal
                if agents_currentCell[i] == self.maze._goal:
                    foundTheGoal[i] = True
                    break

        # PHASE 2
        # Get the pionner index
        pionner = foundTheGoal.index(True)

        # From the article: "Given the path of the agent that was the 
        # first to find the exit, the pioneer, each agent has to find the last location
        # from its own-logged history that matches a location on the path
        # of the pioneer. This location is denoted Last Common Location (LCL)"
        for i in range(0, self.numOfAgents):
            if i == pionner:
                continue

            # Move agent until the last common location with the pionner agent
            comeback_index = -2
            while agents_search[i][-1] != lcl[pionner][i]:
                # Come back unitl the LCL
                agents_search[i].append(effective_path[i][comeback_index])
                comeback_index -= 1

            # Add the path from the last common location until the goal
            lcl_index = effective_path[pionner].index(lcl[pionner][i])
            split_index = lcl_index + 1
            agents_search[i] += effective_path[pionner][split_index:]

        # Get the explored fraction of the maze
        fraction = len(exploredCells) / (self.maze.rows * self.maze.cols)

        return agents_search, fraction
    
    # Return cell children 
    def getChildren(self, cellCoordinate, cellPoints, parent):
        children = []

        for d in "NESW":
            if cellPoints[d] == True:
                if d=='N':
                    childCell = (cellCoordinate[0]-1,cellCoordinate[1])
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='E':
                    childCell = (cellCoordinate[0],cellCoordinate[1]+1)
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='S':
                    childCell = (cellCoordinate[0]+1,cellCoordinate[1])
                    if parent == childCell:
                        continue

                    children.append(childCell)
                elif d=='W':
                    childCell = (cellCoordinate[0],cellCoordinate[1]-1)
                    if parent == childCell:
                        continue

                    children.append(childCell)

        return children


# List of colors of the agents
colorList = [COLOR.red, COLOR.blue, COLOR.yellow, COLOR.orange, COLOR.pink, COLOR.cyan, COLOR.black]

# Size of the maze
numOfLines = 10
numOfColumns = 10

# Number of agents
numOfAgents = 5

# It will be used in the case of loading a specific maze
specificMaze = "somemaze.csv"

# In the case of loading a specific maze with pointed out number of agents. Example: python3 my.py 3 test1
if len(sys.argv) == 3:
    numOfAgents = int(sys.argv[1])
    specificMaze = sys.argv[2] + ".csv"

header = []
steps_row = []
pionner_steps_row = []
fraction_row = []
stdev_row = []

# Only for Tarry's algorithm
steps_from_first_to_last_row = []

# Only for my algorithm
fraction_pionner_row = []
pioneer_after_interval1_row = []
pioneer_after_interval2_row = []
fraction_pioneer_after_interval1_row = []
fraction_pioneer_after_interval2_row = []
fraction_pioneer_in_interval2_row = []
steps_agents_using_interval2_row = []

for i in range(1, 41):

    numOfAgents = i
    header.append(numOfAgents)

    pionner_stepsCount = 0
    stepsCount = 0
    fractionCount = 0
    iterations = 250
    steps_array = []

    # Strange steps
    pioneer_stepsCount_after_interval1 = 0
    pioneer_stepsCount_after_interval2 = 0
    after_interval_1_count = 0
    pioneer_interval2_count = 0
    after_interval_2_count = 0
    steps_agents_using_interval2_count = 0

    # Only for Tarry's algorithm
    steps_from_first_to_lastCount = 0

    # Only for my algorithm
    fraction_pionner_count = 0

    for j in range(0, iterations):

        # Create a instance of a maze
        m=maze(numOfLines,numOfColumns)

        # Create a maze
        m.CreateMaze(theme='light', loadMaze='mazes/40_by_40/maze_40x40__' + str(j+1) + '.csv')
        #m.CreateMaze(theme='light', loadMaze='testperfect3.csv')
        #m.CreateMaze(loopPercent=0,theme='light')
        #m.CreateMaze(loopPercent=0,theme='light', saveMaze=True)

        myAlgorithm = MyAlgorithm(m, numOfAgents, colorList, start=None)
        steps, pionner_steps, fraction, fraction_pionner, pioneer_after_interval1, pioneer_after_interval2, steps_agents_using_interval2 = myAlgorithm.run()

        if pioneer_after_interval1 != 0:
            after_interval_1_count += 1

        if pioneer_after_interval2 != 0:
            after_interval_2_count =+ 1

        if pioneer_after_interval1 != 0 and pioneer_after_interval2 == 0:
            pioneer_interval2_count += 1


        """ tarryGeneralization = TarryGeneralization(m, numOfAgents, colorList, start=None)
        steps, pionner_steps, fraction, last_steps = tarryGeneralization.run() """

        # Free up memory
        m._win.destroy()

        steps_array.append(steps / numOfAgents)

        stepsCount += steps
        pionner_stepsCount += pionner_steps
        fractionCount += fraction

        # Only for Tarry's algorithm
        #steps_from_first_to_lastCount += last_steps - pionner_steps

        # Only for my algorithm
        fraction_pionner_count += fraction_pionner
        pioneer_stepsCount_after_interval1 += pioneer_after_interval1 # Strange steps
        pioneer_stepsCount_after_interval2 += pioneer_after_interval2 # Strange steps
        steps_agents_using_interval2_count += steps_agents_using_interval2 # Strange steps

    # Only for Tarry's algorithm
    """ averageOfStepsFromFirstToLast = steps_from_first_to_lastCount / iterations
    steps_from_first_to_last_row.append(averageOfStepsFromFirstToLast)
    print(numOfAgents, " agents -> average steps from first to last: ", averageOfStepsFromFirstToLast) """

    # Only for my algorithm
    averageFractionPionner = fraction_pionner_count / iterations
    fraction_pionner_row.append(averageFractionPionner)
    print(numOfAgents, " agents -> average of explored fraction until pionner find the goal: ", averageFractionPionner)
    averageOfStepsOfThePionnerAfterInterval1 = pioneer_stepsCount_after_interval1 / iterations
    pioneer_after_interval1_row.append(averageOfStepsOfThePionnerAfterInterval1)
    averageOfStepsOfThePionnerAfterInterval2 = pioneer_stepsCount_after_interval2 / iterations
    pioneer_after_interval2_row.append(averageOfStepsOfThePionnerAfterInterval2)
    print(numOfAgents, " agents -> average of pioneer after interval 1: ", averageOfStepsOfThePionnerAfterInterval1)
    print(numOfAgents, " agents -> average of pioneer after interval 2: ", averageOfStepsOfThePionnerAfterInterval2)
    averageFractionPionnerAfterInterval1 = after_interval_1_count / iterations
    fraction_pioneer_after_interval1_row.append(averageFractionPionnerAfterInterval1)
    averageFractionPionnerAfterInterval2 = after_interval_2_count / iterations
    fraction_pioneer_after_interval2_row.append(averageFractionPionnerAfterInterval2)
    averageFractionPionnerInInterval2 = pioneer_interval2_count / iterations
    fraction_pioneer_in_interval2_row.append(averageFractionPionnerInInterval2)
    print(numOfAgents, " agents -> average of pioneer after interval 1 - fraction: ", averageFractionPionnerAfterInterval1)
    print(numOfAgents, " agents -> average of pioneer after interval 2 - fraction: ", averageFractionPionnerAfterInterval2)
    print(numOfAgents, " agents -> average of pioneer in interval 2 - fraction: ", averageFractionPionnerInInterval2)
    averageStepsAgentsUsingInterval2 = steps_agents_using_interval2_count / numOfAgents / iterations
    steps_agents_using_interval2_row.append(averageStepsAgentsUsingInterval2)
    print(numOfAgents, " agents -> average number of steps of agents using interval 2: ", averageStepsAgentsUsingInterval2)

    averageOfSteps = stepsCount / numOfAgents / iterations
    averageOfStepsOfThePionner = pionner_stepsCount / iterations
    averageOfFraction = fractionCount / iterations
    stdev = statistics.stdev(steps_array)
    print(numOfAgents, " agents -> average number of steps: ", averageOfSteps)
    print(numOfAgents, " agents -> average number of pionner's steps: ", averageOfStepsOfThePionner)
    print(numOfAgents, " agents -> average of explored fraction: ", averageOfFraction)
    print(numOfAgents, " agents -> stdev: ", stdev)

    steps_row.append(averageOfSteps)
    pionner_steps_row.append(averageOfStepsOfThePionner)
    fraction_row.append(averageOfFraction)
    stdev_row.append(stdev)

with open("my_1to40agents_250iterations_40x40_strangepeaks.csv", "w") as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerow(steps_row)
    writer.writerow(pionner_steps_row)
    writer.writerow(fraction_row)
    writer.writerow(stdev_row)

    # Only for Tarry's algorithm
    #writer.writerow(steps_from_first_to_last_row)

    # Only for my algorithm
    writer.writerow(fraction_pionner_row)
    
    writer.writerow(pioneer_after_interval1_row)
    writer.writerow(pioneer_after_interval2_row)
    writer.writerow(fraction_pioneer_after_interval1_row)
    writer.writerow(fraction_pioneer_after_interval2_row)
    writer.writerow(fraction_pioneer_in_interval2_row)
    writer.writerow(steps_agents_using_interval2_row)
















""" bSearch,bfsPath,fwdPath=BFS(m)
a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
bSearch2,bfsPath2,fwdPath2=BFS(m,(5,4))
a2=agent(m,footprints=True,color=COLOR.red,shape='square',filled=True)
m.tracePaths([{a:bSearch}, {a2:bSearch2}],delay=100) """
