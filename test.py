# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 07:48:21 2020

@author: linda
"""


# testing list copies


from copy import deepcopy
a = [
     [1,2,3],
     [4,5,6],
     [7,8,9]
]
c = a
b = deepcopy(a)

print(b[0] in a)



d = [
     [
      [1, 1, 2, 2], [2, 2, 1, 1], [0, 0, 0, 0]
     ], 
     [
      [1, 1, 2, 2], [2, 2, 1, 0], [1, 0, 0, 0]
     ], 
     [
      [1, 1, 2, 2], [2, 2, 1, 1], [0, 0, 0, 0]
     ]
    ]

e = [ [1, 1, 2, 2], [2, 2, 1, 1], [0, 0, 0, 3]]

print(e in d)