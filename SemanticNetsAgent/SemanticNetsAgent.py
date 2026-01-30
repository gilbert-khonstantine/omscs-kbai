from collections import deque

class SemanticNetsAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        self.possible_moves = [(-2, 0), (-1, -1), (0,-2), (-1,0), (0, -1)]
        self.initial_sheep = 0
        self.initial_wolves = 0
        self.verbose = False
    
    def _smart_generator(self, cur_state):
        # consider next possible moves and elimintate those where sheep < wolves
        res = []
        for move in self.possible_moves:
            cur_left_sheeps = cur_state[0]
            cur_left_wolves = cur_state[1]
            cur_location = cur_state[2]
            next_location = cur_location * -1
            next_left_sheeps = cur_left_sheeps + next_location * move[0]
            next_left_wolves = cur_left_wolves + next_location * move[1]
            next_right_sheeps = self.initial_sheep - next_left_sheeps
            next_right_wolves = self.initial_wolves - next_left_wolves
            if self.initial_sheep >= next_left_sheeps >= 0 and self.initial_wolves >= next_left_wolves >= 0 \
                and (next_left_sheeps == 0 or next_left_sheeps >= next_left_wolves) and (next_right_sheeps == 0 or next_right_sheeps >= next_right_wolves):
                res.append((next_left_sheeps, next_left_wolves, next_location))
        return res
    
    def _smart_tester(self, states, visited):
        # eliminate states where its visited already
        res = []
        for state in states:
            if state not in visited:
                res.append(state)
        return res
    
    def _get_path(self, state, parentMap):
        # given a child state, back track to the parent and the steps taken to achieve this
        res = []
        cur = state
        while cur:
            if self.verbose:
                print(cur)
            parent = parentMap[cur]
            if parent:
                sheeps_moved = abs(parent[0] - cur[0])
                wolves_moved = abs(parent[1] - cur[1])
                res.append((sheeps_moved, wolves_moved))
            cur = parent
        res.reverse()
        return res

    def solve(self, initial_sheep, initial_wolves):
        #Add your code here! Your solve method should receive
        #the initial number of sheep and wolves as integers,
        #and return a list of 2-tuples that represent the moves
        #required to get all sheep and wolves from the left
        #side of the river to the right.
        #
        #If it is impossible to move the animals over according
        #to the rules of the problem, return an empty list of
        #moves.
        if initial_sheep < initial_wolves:
            return []
        
        location = -1 # -1 is left of the bank, 1 is right of the bank
        parentMap = {} # hashmap - key is the state and value is the previous state
        visited = set() # this is a set of which state is visited
        start_state = (initial_sheep, initial_wolves, location)
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        res = []
        
        queue = deque()
        
        queue.append(start_state)
        visited.add(start_state)
        parentMap[start_state] = None
        
        while len(queue) > 0:
            cur_state = queue.popleft()
            if cur_state == (0, 0, 1):
                if self.verbose:
                    print(parentMap)
                res = self._get_path(cur_state, parentMap)
                return res
            
            generated_states = self._smart_generator(cur_state=cur_state)
            new_states = self._smart_tester(generated_states, visited)
            if self.verbose:
                print(f"current_state={cur_state} next_states={new_states}")
            for next_state in new_states:
                queue.append(next_state)
                visited.add(next_state)
                parentMap[next_state] = cur_state
        return res
