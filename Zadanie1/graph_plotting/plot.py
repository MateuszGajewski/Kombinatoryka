import matplotlib.pyplot as plt


class Plot:

    def __init__(self):
        pass

    def draw(self, cycles, points):
        cyclea = cycles[0]
        cycleB = cycles[1]

        fig, ax = plt.subplots(1)  # Prepare 2 plots
        ax.set_title('Solutions')
        ax.scatter(points[:, 1], points[:, 2], s = 1)  # plot A
        for i in range(1, len(cyclea)):
            ax.plot([points[cyclea[i-1], 1], points[cyclea[i], 1]],
                    [points[cyclea[i-1], 2], points[cyclea[i], 2]], 'ro-')
        ax.plot([points[cyclea[0], 1], points[cyclea[-1], 1]],
                [points[cyclea[0], 2], points[cyclea[-1], 2]], 'ro-')

        for i in range(1, len(cycleB)):
            ax.plot([points[cycleB[i-1], 1], points[cycleB[i], 1]],
                    [points[cycleB[i-1], 2], points[cyclea[i], 2]], 'bo-')
        ax.plot([points[cycleB[0], 1], points[cycleB[-1], 1]],
                [points[cycleB[0], 2], points[cycleB[-1], 2]], 'bo-')
        plt.show()
