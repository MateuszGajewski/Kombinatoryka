import matplotlib.pyplot as plt
import numpy as np


class Plot:

    def __init__(self, instance_name):
        self.name = instance_name

    def draw(self, cycles, points):
        cyclea = cycles[0]
        cycleb = cycles[1]

        fig, ax = plt.subplots(1)  # Prepare 2 plots
        ax.set_title('Solutions ' + self.name)
        ax.scatter(points.x, points.y)  # plot A

        print(f"Plotting {self.name} with sizes {len(np.unique(cyclea))}, {len(np.unique(cycleb))}")

        for i in range(1, len(cyclea)):
            ax.plot([points.x[cyclea[i-1]], points.x[cyclea[i]]],
                    [points.y[cyclea[i-1]], points.y[cyclea[i]]], 'ro-')
        ax.plot([points.x[cyclea[0]], points.x[cyclea[-1]]],
                [points.y[cyclea[0]], points.y[cyclea[-1]]], 'ro-')

        for i in range(1, len(cycleb)):
            ax.plot([points.x[cycleb[i - 1]], points.x[cycleb[i]]],
                    [points.y[cycleb[i - 1]], points.y[cycleb[i]]], 'bo-')
        ax.plot([points.x[cycleb[0]], points.x[cycleb[-1]]],
                [points.y[cycleb[0]], points.y[cycleb[-1]]], 'bo-')

        plt.show()
