from abc import ABC
import numpy as np
import pandas as pd
from utils.instance_parser.instance_parser import Parser


class EuclideanParser(Parser, ABC):
    dimension = 0
    matrix = np.array([])
    points = None

    def len_between_points(self, pointA, pointB):
        length = (np.sqrt((pointA[1] - pointB[1]) ** 2 + (pointA[2] - pointB[2]) ** 2))
        return length

    def parse_to_matrix(self, points):
        self.matrix = np.zeros([self.dimension, self.dimension])
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if i == j:
                    self.matrix[i][j] = 0
                else:
                    self.matrix[i][j] = self.len_between_points(points[i], points[j])
        self.matrix = np.round(self.matrix)

    def parse(self, filename: str):
        points = pd.read_csv(filename, sep=' ', names=['id', 'x', 'y'], skiprows=6, skipfooter=1, engine='python')

        self.dimension = len(points)
        self.points = points
        self.parse_to_matrix(points.values.tolist())
        return self.matrix

    def get_points(self):
        return self.points
