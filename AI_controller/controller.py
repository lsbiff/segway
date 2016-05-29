# -*- coding: utf-8 -*-
import numpy
from .state import State
import random
import datetime, time
import math

class Controller:
    def __init__(self, game, load, state):
        self.initialize_parameters(game, load, state)
        self.numNeighbors = 10
        self.numPerformances = 10
        self.neighbors = {}
        self.currentPerformances = {}
        self.performanceControl = 0
        self.neighborsControl = 0
        self.currentOption = ()
        self.bestReached = 0
        self.numFile = 0
        self.temperature = 10000
        self.finalIteraction = False

    def initialize_parameters(self, game, load,state):
        self.state = state
        if load == None:
            self.parameters = numpy.random.uniform(0, 1, 3*len(self.compute_features(state)))
            
        else:
            params = open(load, 'r')
            weights = params.read().split("\n")
            self.parameters = [float(x.strip()) for x in weights[0:-1]]
    


    def output(self, episode, performance):
     # print "Performance do episodio #%d: %d" % (episode, performance)
     if episode > 0 and episode % 11 == 0:
            print "Performance do episodio #%d: %d" % (episode/11, performance) 
            output = open("./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'), "w+")
            for parameter in self.parameters:
               output.write(str(parameter) + "\n")

#--------------------------------------------------------------------------------------------------------

    #FUNCAO A SER COMPLETADA. Deve utilizar os pesos para calcular as funções de preferência Q para cada ação e retorna
    #-1 caso a ação desejada seja esquerda, +1 caso seja direita, e 0 caso seja ação nula
    def take_action(self, state):
        features   = self.compute_features(state)
        parameters = numpy.array_split(self.parameters, 3)
        thetaLeft  = parameters[0]
        thetaNeutral   = parameters[1]
        thetaRight = parameters[2]
        
        valueLeft = sum(numpy.multiply(thetaLeft, features))
        valueNeutral = sum(numpy.multiply(thetaNeutral, features))
        valueRight = sum(numpy.multiply(thetaRight, features))


        if valueNeutral >= valueLeft and valueNeutral >= valueRight:
            return 0

        if valueLeft >= valueNeutral and valueLeft >= valueRight:
            return -1

        if valueRight >= valueLeft and valueRight >= valueNeutral:
            return 1

        return 0

    #FUNCAO A SER COMPLETADA. Deve calcular features expandidas do estados (Dica: deve retornar um vetor)
    def compute_features(self, state):
        features = [state.wheel_x, state.rod_angle, state.angular_velocity]
        print "roda     ", state.wheel_x/1200
        print "angulo   ", state.rod_angle/60
        print "ang vel  ", state.angular_velocity/4000
        print "vel_x    ", state.velocity_x
        print "vel_y    ", state.velocity_y

        # rod_angle
        # ngular_velocity
        # wheel_x
        # wind
        # friction
        # velocity_x
        # velocity_y
        # feature1 = state.wheel_x * state.wheel_x
        # feature2 = math.sin(state.rod_angle * state.angular_velocity)
        # feature2 = math.sin(state.rod_angle)
        #feature2 = state.rod_angle * state.angular_velocity
        # feature2 = state.rod_angle * state.rod_angle
        # features = [1, feature2]
        # features = [state.wheel_x * state.rod_angle, state.rod_angle * state.rod_angle, state.angular_velocity]
        # features = [math.cos(state.rod_angle), state.wheel_x]
        # features = [math.cos(state.rod_angle)]
        return features

    # Hill Climbing procurando vizinhos
    #FUNCAO A SER COMPLETADA. Deve atualizar a propriedade self.parameters
    def update(self, episode, performance):
        if self.neighborsControl == self.numNeighbors:
            #print "terminou vizinhos"
            self.neighbors[performance] = self.parameters 
            highestKey = max(self.neighbors.keys())
            #print highestKey
            #print self.neighbors[highestKey]
            if (highestKey > self.currentOption[0]):
                print "trocou"
                self.parameters = self.neighbors[highestKey]
                output = open("./params/%d-%d.txt" % (highestKey, self.numFile), "w+")
                self.numFile+=1
                for parameter in self.parameters:
                    output.write(str(parameter) + "\n")

            self.neighbors.clear()
            self.neighborsControl = 0
        else:
            if self.neighborsControl == 0:
                self.currentOption = (performance, self.parameters)

            else:
                for i in range(len(self.parameters)):
                    self.parameters[i] = self.parameters[i] + numpy.random.uniform(-0.002, 0.002)
                    if self.parameters[i] > 1:
                        self.parameters[i] = 1
                    if self.parameters[i] < 0:
                        self.parameters[i] = 0

            self.neighbors[performance] = self.parameters 
            self.neighborsControl+=1

        pass
