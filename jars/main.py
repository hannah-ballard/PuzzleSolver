# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 08:01:55 2020

@author: hannah
"""
#import sys
from copy import deepcopy
import time
import random


class ClosedList():
    def __init__(self, maxlen=0):
        self._closedList = []
        if maxlen==0:
            self.length = 100
        else:
            self.length = maxlen
        self.index = 0
        
    def Add(self, item):
        #try:
            if len(self._closedList)<self.length:
                self._closedList.append(item)
            else:
                self._closedList[self.index] = item
                self.index = self.index+1
                if self.index==self.length:
                    self.index=0
        #except Exception:
        #    from IPython import embed
        #    embed()
                
    def Contained(self, item):
        return item in self._closedList

def BreadthFirstSearch(initState):

    start = time.perf_counter()
    end = 0
    closedList = ClosedList(maxlen = 1000)
    openList = [initState]
    count = 0
    try:
        while len(openList)>0:
            currentState = openList.pop()
            closedList.Add(currentState.jars)
            if currentState.isSolved:
                end = time.perf_counter()
                statusstr = "Solution Time: "+ str((end-start))[:5] 
                statusstr += " (Open List: "+str(len(openList))
                statusstr += ") Depth: "+str(currentState.depth) 
                print(statusstr)
                return currentState

            for child in currentState.Children:
                if not closedList.Contained(child.jars):
                    openList.insert(0,child)
                    
            count = count+1
            if count %10000==0:
                print("Still searching:"+str(count))
                currentState.PrintJars()
                        

    except KeyboardInterrupt:
        print("early release:")


def DepthFirstSearch(initState):
    count = 0
    fakestate = State([1,2,3])
    fakestate.depth = 1000000000
    ShortestSolution = fakestate
    start = time.perf_counter()
    end = 0
    closedList = ClosedList()
    openList = [initState]
    discardedstatecount = 0
    
    try:
        while len(openList)>0:
            currentState = openList.pop()
            if currentState.depth < ShortestSolution.depth:
                closedList.Add(currentState.jars)
                if currentState.isSolved:
                    ShortestSolution = currentState
                    count = count+1
                    end = time.perf_counter()
                    statusstr = "Solution "+str(count).ljust(5, " ")+" Time: "+ str((end-start))[:5] 
                    statusstr += " (Open List: "+str(len(openList))+") Depth: "+str(ShortestSolution.depth) 
                    statusstr += " Throwaways: " + str(discardedstatecount) 
                    print(statusstr)
                    if (end-start)>10:
                        break
                    start = time.perf_counter()
                    discardedstatecount = 0
                    
                
                for child in currentState.Children:
                    if not closedList.Contained(child.jars):
                        openList.append(child)
                        
                    
            else:
                discardedstatecount = discardedstatecount + 1

    except KeyboardInterrupt:
        print(ShortestSolution.PrintLineage())
    return ShortestSolution


def ChaosSearch(initState):
    count = 0
    fakestate = State([1,2,3])
    fakestate.depth = 1000000000
    ShortestSolution = fakestate
    start = time.perf_counter()
    end = 0
    closedList = ClosedList()
    openList = [initState]
    discardedstatecount = 0

    levels = [0]
    tempstart = time.perf_counter()
    chaoscount = 0
    try:
        while len(openList)>0:
            end = time.perf_counter()
            if (end-tempstart) > 4:
                print("CHAOS")
                chaoscount = chaoscount+1
                openList = [initState]
                tempstart = time.perf_counter()
                if chaoscount>25:
                    break

            if len(openList)>1 and levels[-1] > 2:            
                rand = random.randint(len(openList)-levels[-1], len(openList)-1)
                currentState = openList[rand]
                del openList[rand]
            else:
                currentState = openList.pop()
            if currentState.depth < ShortestSolution.depth:
                closedList.Add(currentState.jars)
                if currentState.isSolved:
                    ShortestSolution = currentState
                    count = count+1
                    end = time.perf_counter()
                    statusstr = "Solution "+str(count).ljust(5, " ")+" Time: "+ str((end-start))[:5] 
                    statusstr += " (Open List: "+str(len(openList))+") Depth: "+str(ShortestSolution.depth) 
                    statusstr += " Throwaways: " + str(discardedstatecount) 
                    print(statusstr)
                    
                    start = time.perf_counter()
                    discardedstatecount = 0
                    tempstart = time.perf_counter()
                    chaoscount = 0
                    
                
                for child in currentState.Children:
                    if not closedList.Contained(child.jars):
                        openList.append(child)
                levels.append(len(currentState.Children))
                        
                    
            else:
                discardedstatecount = discardedstatecount + 1

    except KeyboardInterrupt:
        print(ShortestSolution.PrintLineage())
    return ShortestSolution


class State:
    def __init__(self, jars):
        self.jars = jars
        self.parent = None
        self._children = None
        self._isComplete = None
        self._isSolved = None
        self.depth = 0

    @property
    def isComplete(self):
        if self._isComplete is None:
            self._isComplete = all([x for x in self.jars if State.IsSame(x)])
        return self._isComplete  

    @property
    def Children(self):
        if self._children is None:
            self._children = self.GenerateChildren()
        return self._children
        
    @property
    def isSolved(self):
        if self._isSolved is None:
            for jar in self.jars:
                if not State.IsSame(jar): 
                    self._isSolved = False # jar contains different elements
                    return self._isSolved
            self._isSolved = True
        return self._isSolved

    @staticmethod
    def IsSame(jar):
        return len(set(jar)) == 1
    
    def PrintJars(self, jars=[]):  
        if jars==[]:
            jars = self.jars
        output = "\n"
        for i in range((len(jars[0])-1), -1, -1):
            row = ""
            for jar in jars:
                row += "|" + str(jar[i]).rjust(2,'0') + "|  "
            
            output += row.replace("00","**")+"\n"
            
        output += " " + ("——    "*len(jars)) + "\n"
        output += "Depth: "+str(self.depth)+"\n"
        print( output)
        
    def GenerateChildren(self):
        children = []
        for move in self.PossibleMoves():      
            childJars = deepcopy(self.jars)
            
            fromjar = childJars[move[0]]
            tojar = childJars[move[1]]
            
            
            ballindex = State.TopIndexInJar(fromjar)-1
            arriveindex = State.TopIndexInJar(tojar)
            tojar[arriveindex] = fromjar[ballindex]
            fromjar[ballindex] = 0
            
                
            child = State(childJars)
            child.parent = self
            child.depth = self.depth+1   
            children.append(child)    
            
        return children
    
    def PossibleMoves(self):
        possibleMoves = []
        for i in range(len(self.jars)):
            jar = self.jars[i]
            for j in range(len(self.jars)):
                if i==j:
                    pass
                elif State.CanMove(jar, self.jars[j]):
                    possibleMoves.append((i,j))
        return possibleMoves
    
    @staticmethod
    def TopIndexInJar(jar):
        if 0 not in jar:
            return len(jar)
        return jar.index(0)
        
    
    @staticmethod
    def CanMove(jar1, jar2):
        #can top of jar1 be moved to jar2
        if State.IsSame(jar1): #jar is either completely empty or completed
            return False
        elif State.IsEmpty(jar2): #Jar2 is empty
            return True
        elif State.TopItemInJar(jar1)==State.TopItemInJar(jar2) and not State.IsFull(jar2):
            return True
        else:
            return False
    
    @staticmethod
    def IsEmpty(jar):
        return jar.count(0) == len(jar)
    
    @staticmethod
    def IsFull(jar):
        return jar[-1]!=0
    
    @staticmethod
    def TopItemInJar(jar):
        for i in range((len(jar)-1), -1, -1):
            if jar[i]!=0:
                return jar[i]
        return jar[0]
    
    def PrintLineage(self):
        print("*****************")
        print("printing Lineage")
        print("")
        currentNode = self
        while True:
            currentNode.PrintJars()
            
            if currentNode.parent is None:
                break
            currentNode = currentNode.parent

    def Deepcopy(self):
        copyState = State(deepcopy(self.jars))
        copyState.depth = self.depth
        copyState.parent = self.parent
        return copyState

class StreamlineSolution():
    
    def __init__(self, initSolution):
        self.initSolution = initSolution
        self.initSolution.PrintJars()
        self.initStepsList = StreamlineSolution.getStepsList(initSolution)
        print(self.initStepsList)
        self.shortList = self.streamLineSteps(self.initStepsList)
        print("Initial length: "+str(len(self.initStepsList))+" + New Length: "+str(len(self.shortList)))
        
    def streamLineSteps(self, initList):
        shortList = self.shortenStepsList(self.initStepsList)
        
        for i in range(5):
            shortList = shortList[:i]+self.shortenStepsList(shortList[i:])
            
        return shortList
        
        pass
        
    @staticmethod
    def getStepsList(finalSolution):
        currentNode = finalSolution
        stepsList = []
        while True:
            stepsList.append(currentNode)       
            if currentNode.parent is None:
                break
            currentNode = currentNode.parent                
        stepsList.reverse() # so the initial list is in order first step->last steps
        return stepsList
    
    def shortenStepsList(self, stepsList):
        if len(stepsList)<=2:
            return stepsList
        elif len(stepsList)>6:
            short1 = self.shortenStepsList(stepsList[:5])
            short2 = self.shortenStepsList(stepsList[6:])
            shortenedStepsList = short1+short2
        else:
            shortenedStepsList = self.BreadthFirstSearch(stepsList[0], stepsList[-1])
        if shortenedStepsList is not None:
            return shortenedStepsList
        else:
            return stepsList
    
    def BreadthFirstSearch(self, initState, finalState):        
        start = time.perf_counter()
        end = 0
        closedList = ClosedList(maxlen = 1000)
        openList = [initState]
        count = 0
        try:
            while len(openList)>0:
                currentState = openList.pop()
                closedList.Add(currentState.jars)
                if currentState.jars==finalState.jars:
                    end = time.perf_counter()
                    statusstr = "Solution Time: "+ str((end-start))[:5] 
                    statusstr += " (Open List: "+str(len(openList))
                    statusstr += ") Depth: "+str(currentState.depth)
                    print(statusstr)
                    return self.GetSteps(initState, currentState)
    
                for child in currentState.Children:
                    if not closedList.Contained(child.jars):
                        openList.insert(0,child)
                        
                count = count+1
                if count %10000==0:
                    print("Still searching:"+str(count))
                    currentState.PrintJars()
                            
    
        except KeyboardInterrupt:
            print("early release:")

    def GetSteps(self, initState, currentState):
        stepsList = [currentState]
        tempState = currentState
        count = 0
        while True:
            tempState = tempState.parent
            stepsList.insert(0,tempState)
            if tempState.jars == initState.jars:
                break
            count = count+1
            if count>100:
                for val in stepsList:
                    print(val)
                raise ValueError("count really shouldn't get this high")
        return stepsList.reverse()
        
        
   


def jars0():
    return [
        [1,2],
        [2,1],
        [0,0]
    ]

def jars1():
    return [
        [1,1,2,2],
        [2,2,1,1],
        [0,0,0,0]
    ]

def jars3():
    return [
        [1,2,1,3],
        [2,2,3,1],
        [3,3,1,2],
        [0,0,0,0],
        [0,0,0,0]
    ]

def jars18():
    return[
        [1,2,1,3],
        [4,4,5,6],
        [1,7,6,2],
        [3,3,2,5],
        [7,3,5,5],
        [6,1,6,7],
        [2,4,7,4],
        [0,0,0,0],
        [0,0,0,0]   
    ]

def jars424():
    return [
         [12, 10, 7, 2, 9], 
         [2, 8, 9, 9, 10], 
         [99, 11, 5, 5, 7], 
         [99, 6, 4, 5, 12], 
         [4, 11, 6, 7, 9], 
         [2, 12, 99, 7, 12], 
         [11, 99, 1, 99, 5], 
         [3, 8, 3, 4, 1], 
         [5, 10, 2, 10, 9], 
         [4, 4, 3, 6, 8], 
         [11, 8, 10, 6, 2], 
         [3, 1, 8, 6, 1], 
         [11, 7, 1, 12, 3], 
         [0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0]
     ]

        

def main():      
    #try:
        start = time.perf_counter()
        initState = State(jars424())
        shortestSolution = ChaosSearch(initState)
        #shortestSolution = DepthFirstSearch(initState)
        #shortestSolution = BreadthFirstSearch(initState)
    
        shortestSolution.PrintLineage()
        print("Total Steps: "+str(shortestSolution.depth))
        
        end = time.perf_counter()
        for val in StreamlineSolution(shortestSolution).shortList:
            val.PrintJars()
        
        print("Time to run: "+str((end-start))[:5]+"s")
    #except Exception:
    #    from IPython import embed
    #    embed()
    
if __name__ =="__main__":
    main()