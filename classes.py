import pygame
import random
import os
import sys

def addPath(r_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, r_path)

class Food:
    def __init__(self, type, x):
        self.type = type
        self.x = x
        self.y = 100

class Person:
    def __init__(self, type):
        self.type = type
        self.state = "Walking"
        self.x = -100
        self.targetx = random.randint(20, 140)*5
        self.y = 500
        self.waitTime = random.randint(300, 480)
        self.currTimer = 0