from abc import ABC, abstractmethod
import numpy as np


class Solver(ABC):



    @abstractmethod
    def solve(self, array=np.array):
        pass
