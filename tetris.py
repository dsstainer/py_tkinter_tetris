
import tkinter as tk
import random
import threading
import time

class Board:
    #need to change deletion and remaking to use coords() or move() method instead
    #problem lies with collisions. For example y-axis collisions only work if the structures don't overhang
    def __init__(self):
        #initialise constants
        self.windowHeight = 600
        self.windowWidth = 500
        self.headerHeight = 40
        self.scoreBarWidth = 100
        self.frameLength = 200
        self.tetriminoOffset = 4
        self.tetrisScreenWidth = self.windowWidth-self.scoreBarWidth
        self.tetrisScreenHeight = self.windowHeight-self.headerHeight
        self.numBlocksX = 10
        self.numBlocksY = 20

        #initialise settings for collisions and destructions
        self.heightBoundary = self.numBlocksY - 1
        self.leftBoundary = 0
        self.rightBoundary = self.numBlocksX - 1
        self.collisionBlocks = {}
        self.rowCounts = [0 for x in range(self.numBlocksY)]
        self.score = 0
        self.rowScore = 100

        #size sections of screen
        self.window = tk.Tk() #create window panel by declaring window of class Tk
        
        self.frm_left = tk.Frame(master = self.window,width=self.windowWidth-self.scoreBarWidth, height = self.windowHeight)
        self.frm_header = tk.Frame(master=self.frm_left,width=self.windowWidth-self.scoreBarWidth,height=self.headerHeight)
        self.cv_tetrisScreen = tk.Canvas(master=self.frm_left, width = self.windowWidth-self.scoreBarWidth, height = self.windowHeight-self.headerHeight, bg="white")
        
        self.frm_right = tk.Frame(master=self.window,width=self.scoreBarWidth,height=self.windowHeight)
        self.frm_scoreBar = tk.Frame(master=self.frm_right, width=self.scoreBarWidth, height=self.windowHeight)

        #set up inner components
        self.headerSettings()
        self.tetrisScreenSettings()
        self.scoreBarSettings()

        #add sections to window
        self.frm_header.pack(fill=tk.BOTH)
        self.cv_tetrisScreen.pack(fill=tk.BOTH)
        self.frm_left.pack(fill=tk.BOTH,side=tk.LEFT)

        self.frm_scoreBar.pack(fill=tk.BOTH)
        self.frm_right.pack(fill=tk.BOTH, side=tk.LEFT)

        #run game loop on a seperate thread to manage gameplay
        gameThread = threading.Thread(target=self.gameLoop)
        gameThread.start()#Technically creates a race condition on self.currentTetrimino.currentY/currentX but don't know how to modify
        #run event loop to manage user input
        self.window.mainloop()
        

    def scoreBarSettings(self):
        self.lbl_scoreTitle = tk.Label(master=self.frm_scoreBar, text="Score:\n")
        self.lbl_scoreTitle.config(font=("Courier", 20))
        #self.lbl_levelTitle = 
        #self.lbl_level = 
        self.lbl_score = tk.Label(master=self.frm_scoreBar, text=str(self.score))
        self.lbl_score.config(font=("Courier", 20))
        
        self.lbl_scoreTitle.pack(pady=(30,10))
        self.lbl_score.pack()


    def headerSettings(self):
        self.lbl_title = tk.Label(master = self.frm_header, text="TETRIS")
        self.lbl_title.config(font=("Courier", 20))
        self.lbl_title.pack()


    def tetrisScreenSettings(self):
        #configure grid
        self.blockWidth = (self.tetrisScreenWidth)/self.numBlocksX
        self.blockHeight = (self.tetrisScreenHeight)/self.numBlocksY

        currentWidth = self.blockWidth
        for x in range(9):
            self.cv_tetrisScreen.create_line(currentWidth, 0, currentWidth, self.tetrisScreenHeight)
            currentWidth += self.blockWidth

        currentHeight = self.blockHeight
        for y in range(19):
            self.cv_tetrisScreen.create_line(0, currentHeight,self.tetrisScreenWidth, currentHeight)
            currentHeight += self.blockHeight

        #input settings
        self.window.bind('<Left>', self.handle_left)
        self.window.bind('<Right>', self.handle_right)
        self.window.bind('<Up>', self.handle_up)
        self.window.bind('<Down>', self.handle_down)
        #self.window.bind('<Return>', self.handle_enter)


    def worldToScreen(self,x,y):#world is 0 to 9, 0 to 19. Screen is 0 to tetrisScreenWidth, 0 to tetrisScreenHeight
        screenX = (self.blockWidth*x)
        screenY = (self.blockHeight*y)
        return screenX, screenY

    def screenToWorld(self,x,y):
        worldX = (x//self.blockWidth)
        worldY = (y//self.blockHeight)
        return worldX, worldY
        
                
    def createTetrisBlock(self, x,y, *args):
        x,y = self.worldToScreen(x,y)
        return self.cv_tetrisScreen.create_rectangle(x, y, x+self.blockWidth, y+self.blockHeight, fill="red", tags=(args))
        
        
    def moveCurrentTetriminoDownWorkerThread(self):
        time.sleep(self.frameLength * 0.001) #wait some time
        return self.stepDown()

    def moveCurrentTetriminoDownMainThread(self):
        self.cv_tetrisScreen.after(0, self.stepDown) #wait some time
        

    def stepDown(self): #returns whether collision has occured
        self.cv_tetrisScreen.move("current", 0, self.blockHeight)
        self.currentTetrimino.currentY += 1
        if self.collisionDown():
            self.cv_tetrisScreen.move("current", 0, self.blockHeight*-1)
            self.currentTetrimino.currentY -= 1

            return True
        #else:

            #self.cv_tetrisScreen.move("current", 0, self.blockHeight)
            #self.createCurrentTetrimino()
        return False

    def stepAcross(self, step):
        self.cv_tetrisScreen.move("current", (self.blockWidth*step), 0)
        self.currentTetrimino.currentX += step

        if self.collisionAcross():
            self.cv_tetrisScreen.move("current", (self.blockWidth*step*-1), 0)
            self.currentTetrimino.currentX -= step
        #else:
            #self.cv_tetrisScreen.move("current", (self.blockWidth*step), 0)
            #self.createCurrentTetrimino()

    def stepRotate(self):
        self.currentTetrimino.rotate()
        if self.collisionRotate():
            self.currentTetrimino.unRotate()
        else:
            self.cv_tetrisScreen.delete("current")
            self.createCurrentTetrimino()

    def gameLoop(self):
        self.createNewTetrimino()
        lose = False
        while not lose:
            loop = False
            while not loop:
                loop = self.moveCurrentTetriminoDownWorkerThread() #once it tries to step outside of the screen, the loop exits
            self.handleCollisionDown()
            self.checkRowDestruction()
            self.updateScore()
            self.createNewTetrimino()


    def lose(self):
        self.window.destroy()
            
        

    def updateScore(self):
        self.lbl_score.config(text=str(self.score))

        
    def handleCollisionDown(self):
        for c in self.currentTetrimino.coords:
            #extract info
            x, y = c
            x = x + self.currentTetrimino.currentX
            y = y + self.currentTetrimino.currentY

            #check for game over
            if y <= 0:
                self.lose()

            #construct new tetrimino block
            blockID = self.createTetrisBlock(x, y)
            
            #update collision blocks
            idX = "#"+str(x)
            idY = "#" + str(y)
            if idY not in self.collisionBlocks:
                self.collisionBlocks[idY] = dict()
                
            if idX not in self.collisionBlocks.get(idY):
                self.collisionBlocks[idY][idX] = blockID
                
            #update array of row counts
            self.rowCounts[y] += 1


        #delete old tetrimino
        self.cv_tetrisScreen.delete("current")

            
    def checkRowDestruction(self):
        destructionCount = 0
        
        for index in range(19, -1, -1):
            #print(index, rowCount, self.numBlocksX)
            #destroy rows from index 19 (which corresponds to row 19[lowest]) to accumulate destructionCount
            if self.rowCounts[index] >=  self.numBlocksX:
                destructionCount += 1
                self.score += self.rowScore

                #delete blocks in row:
                for blockKey in self.collisionBlocks.get("#"+str(index)):
                    self.cv_tetrisScreen.delete(self.collisionBlocks.get("#"+str(index)).get(blockKey))                

                #need to do something about changing coords of objects in dict... --> pointers?
                #for i in range(len(self.collisionHeights)):
                    #self.collisionHeights[i] += 1
                #delete all coords from hash table in that row and shift down by destructionCount
                del self.collisionBlocks["#"+str(index)]
                
            
            else:
                if destructionCount > 0:
                    #move the rows down depending on their tags



                    self.rowCounts[index+destructionCount] = self.rowCounts[index]

                    if "#"+str(index) in self.collisionBlocks:
                        for blockKey in self.collisionBlocks.get("#"+str(index)):
                            self.cv_tetrisScreen.move(self.collisionBlocks.get("#"+str(index)).get(blockKey), 0, self.blockHeight*destructionCount)

                        self.collisionBlocks["#"+str(index+destructionCount)]=self.collisionBlocks.pop("#"+str(index))



        for x in range(destructionCount):
            self.rowCounts[x] = 0


    def collisionAcross(self):#possible optimisation?
        for c in self.currentTetrimino.coords:
            x, y = c
            x = x + self.currentTetrimino.currentX
            y = y + self.currentTetrimino.currentY

            
            if x < self.leftBoundary or x > self.rightBoundary:
                return True

            if "#"+str(y) in self.collisionBlocks:
                if "#"+ str(x) in self.collisionBlocks.get("#"+str(y)):
                    return True

        return False

    def collisionRotate(self):#possible optimisation?
        for c in self.currentTetrimino.coords:
            x, y = c
            x = x + self.currentTetrimino.currentX
            y = y + self.currentTetrimino.currentY
            if x < self.leftBoundary or x > self.rightBoundary or y > self.heightBoundary  :
                return True

            if "#"+str(y) in self.collisionBlocks:
                if "#"+ str(x) in self.collisionBlocks.get("#"+str(y)):
                    return True

            
        return False

    def collisionDown(self):#possible optimisation?
        for c in self.currentTetrimino.coords:
            x, y = c
            x = x + self.currentTetrimino.currentX
            y = y + self.currentTetrimino.currentY
            if y > self.heightBoundary:
                return True


            if "#"+str(y) in self.collisionBlocks:
                if "#"+ str(x) in self.collisionBlocks.get("#"+str(y)):
                    return True

            
        return False
        
    def createCurrentTetrimino(self):
        for rectCoords in self.currentTetrimino.coords:
            x,y = rectCoords
            self.createTetrisBlock(self.currentTetrimino.currentX+x,self.currentTetrimino.currentY+y, "current")

    def createNewTetrimino(self):
        self.currentTetrimino = Block(self.tetriminoOffset, 0)
        self.createCurrentTetrimino()

    #def handle_enter(self, event):
        #self.createNewTetrimino()
        #self.moveTetrisBlockDown(random.randint(0,9),0, t)

    def handle_up(self, event):
        self.stepRotate()
    
    def handle_down(self, event):
        self.moveCurrentTetriminoDownMainThread()

    def handle_left(self, event):
        self.stepAcross(-1)

    def handle_right(self, event):
        self.stepAcross(1)


class Block:
    #tetrimino space starts from 0,0 at the top corner. Each coordinate is the top left of a sqaure
    """
    tLeftL = [(0,0),(1,0),(2,0),(0,1)]
    tRightL = [(0,0),(1,0),(2,0),(2,1)]
    tBox = [(0,0),(1,0),(0,1),(1,1)]
    tLine = [(0,0),(1,0),(2,0),(3,0)]
    tZigL = [(0,0),(1,0),(1,1),(2,1)]
    tZigR = [(1,0),(2,0),(0,1),(1,1)]
    """

    #update, tetriminos now start with 0,0 being the centre of rotation and always third in the list. This makes rotation calculations way easier
    #quick tip: Up = -ve, Left = -ve
    tLeftL = [(0,1),(1,0),(0,0),(2,0)]
    tRightL = [(-2,0),(-1,0),(0,0),(0,1)]
    tBox = [(-1,-1),(0,-1),(0,0),(-1,0)]
    tLine = [(-2,0),(-1,0),(0,0),(1,0)]
    tZigL = [(-1,0),(0,-1),(0,0),(1,-1)]
    tZigR = [(-1,-1),(0,-1),(0,0),(1,0)]
    tTShape = [(-1,0),(0,-1), (0,0), (1,0)]
    
    
    
    tetriminoes = [tLeftL, tRightL, tBox, tLine, tZigL, tZigR, tTShape]
    
    def __init__(self, currentX, currentY):
        self.coords = self.generateRandomBlockType()
        self.currentX = currentX #The origin of the tetrimino (i.e. where 0,0 in tetrimino space is in world space) are given by currentX and currentY
        self.currentY = currentY

    
    def generateRandomBlockType(self):
        return Block.tetriminoes[random.randint(0,6)]
    """
    
    def generateRandomBlockType(self):
        return Block.tLine
    """
    

    def rotate(self):
        for index,pair in enumerate(self.coords):
            x,y = pair
            xNew = -y
            yNew = x
            self.coords[index] = (xNew, yNew)

    def unRotate(self):
        for index,pair in enumerate(self.coords):
            x,y = pair
            xNew = y
            yNew = -x
            self.coords[index] = (xNew, yNew)

        
        
        
        
b = Board()

