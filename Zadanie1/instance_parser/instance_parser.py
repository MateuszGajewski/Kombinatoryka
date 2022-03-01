from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, filename=str):
        pass
