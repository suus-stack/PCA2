# Eerste simulatie is random laten bewegen  
# implement the two basic principles of escape of and attraction

# stap 1: eerst dat de visjes binnen een bepaalde afstand van elkaar blijven 
# niet meer dan 

# aanpak 1: via coordinaten systeem en dan verschillende snelheid
# aanpak 2: moore neighbourhood

# data: 
# geo
# percepetion length 
# find realistic values for these parameters 
# make a parameter not constant (maybe change over the day nightitme they see less)
# small amount of randomness into perception length (random fluctuation =)
# oval body, circle shape, connecting two ponds 
# agents cannot move out agent based models support boundaries (opzoeken en onderbouwen)
# is strategy still valid in different sizes of pools 


# 1. zorgen dat de vissen een bepaalde afstand tot elkaar bewaren 
# 2. gedragsregels voor vissen implementeren 
# ze kunnen dezelfde positie op het grid hebben (transparency hoog)
import matplotlib
import matplotlib.pyplot as plt
import math
import random
import numpy as np

class Creature():
    def __init__(self, pos_x, pos_y, angle):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.speed = 0.01

    def distance(self, other):
        """
        This method returns the Eucladian distance between one creature and another.
        """
        distance = (self.pos_x - other.pos_x)**2 + (self.pos_y - other.pos_y)**2
        eucl_distance = np.sqrt(distance)
        return eucl_distance
    
    def step(self, other=None):
        """
        The step function updates the coordinates of a creature, ensuring the
        movement of creatures in the simulation.
        """
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed

        # The location of the predator does not depend on another creature (yet)
        if other == None:
            self.pos_x += dx
            self.pos_y += dy
        # The location of the herring depends on its closest neighbour
        else:
            self.pos_x = other.pos_x + dx
            self.pos_y = other.pos_y + dy

        self.pos_x %= 1
        self.pos_y %= 1

    def interact(self):
        pass

    def escape(self):
        pass

class Herring(Creature):
    def __init__(self, pos_x, pos_y, angle, perception_length):
        super().__init__(pos_x, pos_y, angle)
        self.perception_length = perception_length
        self.color = 'blue'
        self.marker = 'o'

    def step(self, other):
        # When a creature crosses a boundary it returns the other way around (torus)
        super().step(other)

    def __repr__(self):
        return f'Herring: {self.pos_x}, {self.pos_y}'

class Predator(Creature):
    def __init__(self, pos_x, pos_y, angle, perception_length):
        super().__init__(pos_x, pos_y, angle)
        self.perception_length = perception_length
        self.color = 'red'
        self.marker = 'D'

    def __repr__(self):
        return f'Predator: {self.pos_x}, {self.pos_y}'

    def step(self):

        # When a creature crosses a boundary it returns the other way around (torus)

        super().step()

class Experiment(Creature):
    def __init__(self, iterations, nr_herring, nr_predators, visualize=True):
        self.iterations = iterations
        self.nr_herring = nr_herring
        self.nr_predators = nr_predators
        self.herring = []
        self.predators = []
        self.visualize = True
        self.add_herring(nr_herring)
        self.add_predators(nr_predators)

        if self.visualize == True:
            self.setup_plot()

    def add_herring(self, nr_herring):
        for _ in range(self.nr_herring):
            pos_x_h = random.uniform(0,1)
            pos_y_h = random.uniform(0,1)
            angle_h = random.uniform(0,1) * math.pi
            herring = Herring(pos_x_h, pos_y_h, angle_h, perception_length=None)
            self.herring.append(herring)
        

    def add_predators(self, nr_predators):
         for _ in range(self.nr_predators):
            pos_x_p = random.uniform(0,1)
            pos_y_p = random.uniform(0,1)
            angle_p = random.uniform(0,1) * math.pi
            predator = Predator(pos_x_p, pos_y_p, angle_p, perception_length=None)
            self.predators.append(predator)

    
    def step(self):
        for herring1 in self.herring:
            min_distance = math.inf
            for herring2 in self.herring:
                if herring1 != herring2:
                    distance = herring1.distance(herring2)
                    # Finding the closest herring
                    if distance < min_distance:
                        min_distance = distance
                        closest_neighbour = herring2

            herring1.step(closest_neighbour)

        for predator in self.predators:
            predator.step()

    def draw(self):
            """
            This function creates the axes along which the creatures move and with
            that the simulation frame, the creatures are plotted making use of
            a scatterplot.
            """

            # Plot range is from 0 to 1 for both x and y axis 
            self.ax1.axis([0, 1, 0, 1])
            self.ax1.set_facecolor((0.7, 0.8, 1.0))
            coordinates_x_h = []
            coordinates_y_h = []
            coordinates_x_p = []
            coordinates_y_p = []

            for herring in self.herring:
                coordinates_x_h.append(herring.pos_x)
                coordinates_y_h.append(herring.pos_y)
                marker_herring = herring.marker
                color_herring = herring.color

            for predator in self.predators:
                coordinates_x_p.append(predator.pos_x)
                coordinates_y_p.append(predator.pos_y)
                marker_predator = predator.marker
                color_predator = predator.color
            

            # Achteraf nog aparte creature lijsten maken zodat je aparte markers en groottes kan kiezen
            self.ax1.scatter(coordinates_x_h, coordinates_y_h, c=color_herring, alpha=0.5, marker=marker_herring)
            self.ax1.scatter(coordinates_x_p, coordinates_y_p, c=color_predator, alpha=0.5, marker=marker_predator, s=150)
            plt.title(f'Simulation of herring school with {self.nr_herring} herring and {self.nr_predators} predator(s)')
            plt.draw()
            plt.pause(0.01) 
            self.ax1.cla()

    def run(self):

        for i in range(self.iterations):
            self.step()

            if self.visualize == True:
                self.draw()

    def setup_plot(self):
            self.fig, self.ax1 = plt.subplots(1)
            self.ax1.set_aspect('equal')
            self.ax1.axes.get_xaxis().set_visible(False)
            self.ax1.axes.get_yaxis().set_visible(False)

if __name__ == "__main__":
    my_experiment = Experiment(1000, 100, 1)
    my_experiment.run()