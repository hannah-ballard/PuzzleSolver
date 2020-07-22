# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:40:23 2020

https://www.youtube.com/watch?v=6edibwHBDFk
Original C# code that was converted to Python

https://murhafsousli.github.io/8puzzle/#/
(ConvertNumbering needed for puzzles supplied from this URL)

@author: Hannah Ballard

0,5,3,1,8,6,2,4,7
time for list based: 510s  8tilepuzzlevideo
time for tuple based: 364s 8tilesolver
time for tuple based w/ global : 235s 8tilesolver2
"""
import sys
import time

ClosedList = []

class Node():
   
    pparent = None #contains parent Node
    puzzle = [] #contains current State of puzzle
    cols = 3
    
    def __init__(self, p):
        self.puzzle = p
        self.children = [] #contains list of Nodes
        self.children[:] = []
        
    def ExpandMove(self):       
        x = self.puzzle.index(0)  

        self.MoveRight(x)
        self.MoveLeft(x)
        self.MoveUp(x)
        self.MoveDown(x)        

        if len(self.children)>8:
            sys.exit(1)
        
    def MoveRight(self, i):
        if i%self.cols < self.cols-1:
            puzzleChild = self.puzzle.copy()
            
            temp = puzzleChild[i+1]
            puzzleChild[i+1] = puzzleChild[i]
            puzzleChild[i] = temp
            
            self.AddChild(puzzleChild)
    
    def MoveLeft(self, i):
        if i%self.cols>0:
            puzzleChild = self.puzzle.copy()
            
            temp = puzzleChild[i-1]
            puzzleChild[i-1]=puzzleChild[i]
            puzzleChild[i] = temp
            
            self.AddChild(puzzleChild)
    
    def MoveUp(self, i):
        if i-self.cols>=0:
            puzzleChild = self.puzzle.copy()
            
            temp = puzzleChild[i-self.cols]
            puzzleChild[i-self.cols]=puzzleChild[i]
            puzzleChild[i] = temp
            
            self.AddChild(puzzleChild)
    
    def MoveDown(self, i):
        if i+self.cols<len(self.puzzle):
            puzzleChild = self.puzzle.copy()
            
            temp = puzzleChild[i+self.cols]
            puzzleChild[i+self.cols]=puzzleChild[i]
            puzzleChild[i] = temp
            
            self.AddChild(puzzleChild)
    
    def AddChild(self, puzzleChild):   
        global ClosedList
        child = Node(puzzleChild)
        child.parent = self
        if tuple(child.puzzle) not in ClosedList:
            self.children.append(child)
        #from IPython import embed
        #embed()
        
    def PrintPuzzle(self):
        print("*****")
        outArr = []
        for row in range(self.cols):
            outArr.append("")

        for i in range(self.cols):
            for j in range(self.cols):
                outArr[j] = outArr[j] + str(self.puzzle[i+(self.cols*j)]) + " "
                
        for j in range(self.cols):
                outArr[j] = outArr[j] + "*"     
                
        for child in self.children:
            for j in range(self.cols):
                outArr[j] = outArr[j] + "| "

            for i in range(self.cols):
                for j in range(self.cols):
                    outArr[j] = outArr[j] + str(child.puzzle[i+(self.cols*j)]) + " "

        for item in outArr:
            print(item)
            
    def IsSamePuzzle(self, p):      
        return self.puzzle == p
        

    def GoalTest(self):
        return self.puzzle == sorted(self.puzzle)
    
    def __eq__(self, other):
        return self.puzzle == other.puzzle


def BreadthFirstSearch(root):
    global ClosedList
    PathToSolution = []
    OpenList = []
    
    OpenList.append(root)
    goalFound = False
    
    while len(OpenList)>0 and not goalFound:
        currentNode = OpenList.pop()
        ClosedList.append(tuple(currentNode.puzzle))
        
        currentNode.ExpandMove()
        """print("******parent********")
        if hasattr(currentNode, "parent"):
            currentNode.parent.PrintPuzzle()
        print("**********endparent**********")
        currentNode.PrintPuzzle()"""


        for child in currentNode.children:
            if child.GoalTest():
                print("found solution!")
                goalFound = True
                PathToSolution = PathTrace(child)
                return goalFound, PathToSolution
            
            elif not Contains(OpenList, child):
                OpenList.insert(0,child)
                
    return goalFound, PathToSolution


def PathTrace(current):
    print("Tracing Path...")
    solutionpath = []
    solutionpath.append(current)

    while hasattr(current, "parent"):
        current = current.parent
        solutionpath.append(current)
        
    return solutionpath
    

def Contains(listOfNodes, node):
    for tempNode in listOfNodes:
        if tempNode == node:
            return True
        
    return False

def convertNumbering(puzzle): 
    #converts the numbering used by most 8-tile programs to the numbering used by this one
    output = puzzle.copy()
    switcher = {
        1:8,
        2:7,
        3:6,
        4:5,
        5:4,
        6:3,
        7:2,
        8:1,
        0:0
    }
    for i in range(len(output)):
        output[i] = switcher.get(output[i])
    return output

def main():
    start = time.perf_counter()
    #puzzle = [1,2,4,3,0,5,7,6,8]                   #medium
    #puzzle = #[1,2,0,3,4,5,6,7,8]                    #easy
    #puzzle = convertNumbering([7,5,8,2,1,3,4,6,0]) #hard
    puzzle = convertNumbering([0,5,3,1,8,6,2,4,7]) #hard
    initNode = Node(puzzle)
    goalFound, pathtosolution = BreadthFirstSearch(initNode)
    if goalFound:
        print("Success!")
        for item in pathtosolution:
            item.PrintPuzzle()
    else:
        print("NOT SUCCESSFUL")
    end = time.perf_counter()
    
    print("Time to run: %s", str((end-start)))

if __name__=="__main__":
    main()