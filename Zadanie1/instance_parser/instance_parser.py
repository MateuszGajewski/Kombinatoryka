from abc import ABC, abstractmethod
import numpy as np


class Parser(ABC):
    dimension = 0
    matrix = np.array([])

    @abstractmethod
    def parse(self, filename: str):
        pass
