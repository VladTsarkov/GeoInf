import random
import numpy as np
import cv2

class Character:
    def __init__(self,x,y,wall):
        self.x = x
        self.y = y
        self.who = "Character"
        wall[self.x][self.y] = 1
        self.density = 0
        self.den_list = []

    #def step(self, wall,temp,density):
    def step(self, wall):
        #for i in range(8):
        self.density += 1
        #temp = temp
        if len(self.den_list) == 0:
            #print("first")
            if wall[self.x - 1][self.y] != 1:
                wall[self.x - 1][self.y] = 1
                self.den_list.append([self.x-1,self.y])
            if wall[self.x + 1][self.y] != 1:
                wall[self.x + 1][self.y] = 1
                self.den_list.append([self.x+1,self.y])
            if wall[self.x][self.y - 1] != 1:
                wall[self.x][self.y - 1] = 1
                self.den_list.append([self.x,self.y-1])
            if wall[self.x][self.y + 1] != 1:
                wall[self.x][self.y + 1] = 1
                self.den_list.append([self.x,self.y+1])
            if wall[self.x - 1][self.y - 1] != 1:
                wall[self.x - 1][self.y - 1] = 1
                self.den_list.append([self.x-1,self.y-1])
            if wall[self.x - 1][self.y + 1] != 1:
                wall[self.x - 1][self.y + 1] = 1
                self.den_list.append([self.x-1,self.y+1])
            if wall[self.x + 1][self.y - 1] != 1:
                wall[self.x + 1][self.y - 1] = 1
                self.den_list.append([self.x+1,self.y-1])
            if wall[self.x + 1][self.y + 1] != 1:
                wall[self.x + 1][self.y + 1] = 1
                self.den_list.append([self.x+1,self.y+1])
            # self.density += 1
        else:
            #print("non")
            temp = []
            #print(self.den_list)

            for i in self.den_list:

                if wall[i[0] - 1][i[1]] == 0 or wall[i[0] - 1][i[1]] > self.density:
                    wall[i[0] - 1][i[1]] = self.density
                    temp.append([i[0]-1,i[1]])
                if wall[i[0] + 1][i[1]] == 0 or wall[i[0] + 1][i[1]] > self.density:
                    wall[i[0] + 1][i[1]] = self.density
                    temp.append([i[0]+1,i[1]])
                if wall[i[0]][i[1] - 1] == 0 or wall[i[0]][i[1] - 1] > self.density:
                    wall[i[0]][i[1] - 1] = self.density
                    temp.append([i[0],i[1]-1])
                if wall[i[0]][i[1] + 1] == 0 or wall[i[0]][i[1] + 1] > self.density:
                    wall[i[0]][i[1] + 1] = self.density
                    temp.append([i[0],i[1]+1])
                if wall[i[0] - 1][i[1] - 1] == 0 or wall[i[0] - 1][i[1] - 1] > self.density:
                    wall[i[0] - 1][i[1] - 1] = self.density
                    temp.append([i[0]-1,i[1]-1])
                if wall[i[0] - 1][i[1] + 1] == 0 or wall[i[0] - 1][i[1] + 1] > self.density:
                    wall[i[0] - 1][i[1] + 1] = self.density
                    temp.append([i[0]-1,i[1]+1])
                if wall[i[0] + 1][i[1] - 1] == 0 or wall[i[0] + 1][i[1] - 1] > self.density:
                    wall[i[0] + 1][i[1] - 1] = self.density
                    temp.append([i[0]+1,i[1]-1])
                if wall[i[0] + 1][i[1] + 1] == 0 or wall[i[0] + 1][i[1] + 1] > self.density:
                    wall[i[0] + 1][i[1] + 1] = self.density
                    temp.append([i[0]+1,i[1]+1])
            #self.density += 1
            self.den_list = temp
            #print(self.den_list)
            #print(self.density)
        # self.density += 1
        return len(self.den_list), self.density - 1
