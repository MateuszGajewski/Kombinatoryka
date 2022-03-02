from abc import ABC
from Zadanie1.instance_parser.instance_parser import Parser


class EuclideanParser(Parser, ABC):
    def open(self, tspfile):
        for line in tspfile:
            line = line.split(" ")
    def parse(self, filename=str):
        pass

