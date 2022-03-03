from abc import ABC
import numpy as np
from Zadanie1.instance_parser.instance_parser import Parser





class EuclideanParser(Parser, ABC):
    dimension = 0
    matrix = 0

    def len_between_points(self, pointA, pointB):
        length = (np.sqrt((pointA[1] - pointB[1]) ** 2 + (pointA[2] - pointB[2]) ** 2))
        return length

    def check(self, file):
        for line in file:
            keywords = line.split()
            print(keywords)
            if keywords[0] == "EDGE_WEIGHT_TYPE" and keywords[2] != "EUC_2D":
                raise NotImplementedError
            if keywords[0] == "DIMENSION:":
                self.dimension = int(keywords[1])
            if keywords[0] == "NODE_COORD_SECTION":
                return

    def parse_to_matrix(self, points):
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if i == j:
                    self.matrix[i][j] == 0
                else:
                    self.matrix[i][j] = self.len_between_points(points[i], points[j])
        self.matrix = np.round(self.matrix)

    def parse_points(self, file):
        self.matrix = np.zeros([self.dimension, self.dimension])
        points = np.zeros([self.dimension, 3], dtype=int)

        for line in file:
            point = line.split()
            if point[0] == "EOF":
                break
            print(point)
            points[int(point[0]) - 1][0] = int(point[0])
            points[int(point[0]) - 1][1] = int(point[1])
            points[int(point[0]) - 1][2] = point[2]
        return points

    def parse(self, filename=str):
        tspfile = open(filename, 'r')
        self.check(tspfile)
        points = self.parse_points(tspfile)
        self.parse_to_matrix(points)
        return self.matrix
