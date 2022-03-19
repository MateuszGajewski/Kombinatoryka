class Edge:
    def __init__(self, v1, v2, matrix):
        self.v1 = v1
        self.v2 = v2
        self.cost = matrix[v1][v2]
