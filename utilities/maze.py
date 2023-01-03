from random import random, randint
from colorama import Fore
from PIL import Image
import numpy as np

class Maze:
  __cell = 'c'
  __unvisited = 'u'
  __maze = []
  __walls = []

  def __init__(self, height: int, width:int):
    self.__height = height
    self.__width = width
    self.__generate()

  def getMaze(self) -> list:
    return self.__maze
  
  def printMaze(self):
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'u'):
          print(Fore.WHITE + str(self.__maze[i][j]), end=" ")
        elif (self.__maze[i][j] == 'c'):
          print(Fore.GREEN + str(self.__maze[i][j]), end=" ")
        else:
          print(Fore.RED + str(self.__maze[i][j]), end=" ")
        
      print('\n')
  
  def getTiff(self):

    a = np.zeros((self.__height,self.__width,3), dtype=np.int8)

    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'c'):
          a[i,j]=[255,255,255]
        else:
          a[i,j]=[0,0,0]

    im = Image.fromarray(a,mode="RGB")
    im.save("./prova.tiff")
    print(a.shape)
    print(im.info)

  # Find number of surrounding cells
  def __surroundingCells(self, rand_wall):
    s_cells = 0
    if (self.__maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.__maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
      s_cells += 1
    if (self.__maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
      s_cells +=1
    if (self.__maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
      s_cells += 1

    return s_cells

  def __markUpperAsWall(self,rand_wall):
    if (rand_wall[0] != 0):
      if (self.__maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]-1][rand_wall[1]] = 'w'
      if ([rand_wall[0]-1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]-1, rand_wall[1]])

  def __markLeftAsWall(self,rand_wall):
    if (rand_wall[1] != 0):
      if (self.__maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]-1] = 'w'
      if ([rand_wall[0], rand_wall[1]-1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]-1])

  def __markRightAsWall(self,rand_wall):
    if (rand_wall[1] != self.__width-1):
      if (self.__maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        self.__maze[rand_wall[0]][rand_wall[1]+1] = 'w'
      if ([rand_wall[0], rand_wall[1]+1] not in self.__walls):
        self.__walls.append([rand_wall[0], rand_wall[1]+1])

  def __markBottomAsWall(self,rand_wall):
    if (rand_wall[0] != self.__height-1):
      if (self.__maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        self.__maze[rand_wall[0]+1][rand_wall[1]] = 'w'
      if ([rand_wall[0]+1, rand_wall[1]] not in self.__walls):
        self.__walls.append([rand_wall[0]+1, rand_wall[1]])
  
  def __deleteWall(self, rand_wall):
    for wall in self.__walls:
      if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        self.__walls.remove(wall)

  
  
  def __generate(self):
    # Denote all cells as unvisited
    # Create an empty list of list (matrix) with height x width dimension
    for i in range(0, self.__height):
      line = []
      for j in range(0, self.__width):
        line.append(self.__unvisited)
      self.__maze.append(line)

    # Randomize starting point and set it a cell
    # Generate a random point inside the list of list (matrix)
    # The starting point must not be in the corner of the matrix
    # so range over 1 to width-2 and 1 to height-2
    starting_height = randint(1,(self.__height-2))
    starting_width = randint(1,(self.__width-2))

    # Mark it as cell and add surrounding walls to the list
    self.__maze[starting_height][starting_width] = self.__cell
    self.__walls.append([starting_height - 1, starting_width])
    self.__walls.append([starting_height, starting_width - 1])
    self.__walls.append([starting_height, starting_width + 1])
    self.__walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    self.__maze[starting_height-1][starting_width] = 'w'
    self.__maze[starting_height][starting_width - 1] = 'w'
    self.__maze[starting_height][starting_width + 1] = 'w'
    self.__maze[starting_height + 1][starting_width] = 'w'

    while (self.__walls):
      # Pick a random wall
      rand_wall = self.__walls[int(random()*len(self.__walls))-1]

      # Check if it is a left wall
      if (rand_wall[1] != 0):
        if (self.__maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.__maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
          # Find the number of surrounding cells
          s_cells = self.__surroundingCells(rand_wall)

          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markUpperAsWall(rand_wall)
            self.__markBottomAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
          

          # Delete wall
          self.__deleteWall(rand_wall)

          continue

      # Check if it is an upper wall
      if (rand_wall[0] != 0):
        if (self.__maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.__maze[rand_wall[0]+1][rand_wall[1]] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markUpperAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
            self.__markRightAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)

          continue

      # Check the bottom wall
      if (rand_wall[0] != self.__height-1):
        if (self.__maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.__maze[rand_wall[0]-1][rand_wall[1]] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            self.__markBottomAsWall(rand_wall)
            self.__markLeftAsWall(rand_wall)
            self.__markRightAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)


          continue

      # Check the right wall
      if (rand_wall[1] != self.__width-1):
        if (self.__maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.__maze[rand_wall[0]][rand_wall[1]-1] == 'c'):

          s_cells = self.__surroundingCells(rand_wall)
          if (s_cells < 2):
            # Denote the new path
            self.__maze[rand_wall[0]][rand_wall[1]] = 'c'
            # Mark the new walls
            self.__markRightAsWall(rand_wall)
            self.__markBottomAsWall(rand_wall)
            self.__markUpperAsWall(rand_wall)

          # Delete wall
          self.__deleteWall(rand_wall)

          continue

      # Delete the wall from the list anyway
      self.__deleteWall(rand_wall)
      
    # Mark the remaining unvisited cells as walls
    for i in range(0, self.__height):
      for j in range(0, self.__width):
        if (self.__maze[i][j] == 'u'):
          self.__maze[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, self.__width):
      if (self.__maze[1][i] == 'c'):
        self.__maze[0][i] = 'c'
        break

    for i in range(self.__width-1, 0, -1):
      if (self.__maze[self.__height-2][i] == 'c'):
        self.__maze[self.__height-1][i] = 'c'
        break



    