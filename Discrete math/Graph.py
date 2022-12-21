class Graph:
    def __init__(self):
        self.graph_exist = False
        self.crt_modulus_exist = False
        self.crt_number_exist = False
  
    def _is_arg_number(x: int):
        return isinstance(x, int) and x > 0

    def create_graph(self, n: int, edges: list, is_undirected=True) -> None:
        '''
        n - number of vertices
        edges - list of tuples (a, b), that indicate in graph there are edge from a to b
        Vertices numbered from 1 to n inclusively
        Return False if n does not positive integer or edges does not match the format
        '''
        self.graph_exist = False
        if not Graph._is_arg_number(n):
            return 
        for i in edges:
            try:
                if len(i) != 2 or not Graph._is_arg_number(i[0]) or not Graph._is_arg_number(i[1]):
                    return
            except:
                return

        self.n = n 

        # Adjacency list of graph
        self.graph = [[] for _ in range(n+1)]

        for a, b in edges:
            self.graph[a].append(b)
            if is_undirected:
                self.graph[b].append(a)

        self.graph_exist = True

    def dfs_order(self, start: int):
        '''
        Return list of vertices how they will be visited by depth-first search (dfs)
            starting with start vertex
        If was error in initializing graph or start vertex doesn't exist, return False
        '''
        if not self.graph_exist:
            return False
        if not Graph._is_arg_number(start) or start > self.n:
            return False

        return self.__dfs(start, [False]*(self.n+1))

    def __dfs(self, cur: int, was: list):
        '''
        Actual dfs algorithm
        cur - current vertex in dfs
        was - list of bool valuies, where was[i] indicate was i-th vertex visited
        ret - initially empty list, we will add vertex there when we visit it
        '''
        was[cur] = True
        ret = [cur]
        for next in self.graph[cur]:
            if not was[next]:
                ret += self.__dfs(next, was)
        return ret

    def bfs_order(self, start: int):
        '''
        Return list of vertices how they will be visited by breadth-first search (bfs)
            starting with start vertex
        If was error in initializing graph or start vertex doesn't exist, return False
        '''
        if not self.graph_exist:
            return False
        if not Graph._is_arg_number(start) or start > self.n:
            return False

        was = [False]*(self.n+1)
        stack = [start]
        was[start] = True
        ret = []

        while len(stack) > 0:
            # get and delete last unvisited vertex
            cur = stack.pop(-1)

            # mark vertex as visited
            ret.append(cur)

            for next in self.graph[cur]:
                if not was[next]:
                    was[next] = True
                    stack.append(next)
        return ret