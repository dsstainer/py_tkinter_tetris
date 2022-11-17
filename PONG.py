import random
import math
class Paddle:

    ######CONSTRUCTION#####
    
    def __init__(self,root,board, upBindKey, downBindKey, right ,fillColour="white"):#left is a variable which indicates whether a paddle is on the left or right of the board. False = left, True = right
        #set attributes - board dimension dependant
        self.WIDTH = board.getPaddleWidth()
        self.HEIGHT = board.getPaddleHeight()
        self.X_COORD = self.calculateXCoord(board, right)#this depends on which side the paddle is places
        
        self.yCoord = board.getPaddleDistanceY()
        self.MOVEMENT_DISTANCE = board.getMovementDistance()

        #set attributes - user requirement dependant
        self.UP_BIND_KEY = upBindKey
        self.DOWN_BIND_KEY = downBindKey
        self.FILL_COLOUR = fillColour
        self.RIGHT = right

        #bind keys to methods
        self.bindKeys(root, board)

         #draw paddle in initial position and store id
        self.PADDLE_ID = self.drawPaddle(board)

    def bindKeys(self,root, board):
        root.bind(self.UP_BIND_KEY, self.moveUp, board) #we need the canvas to update stuff on the canvas
        root.bind(self.DOWN_BIND_KEY, self.moveDown, board)


    #the paddle must be drawn inside the board! validation required
    #drawPaddle returns the id of our tkinter widget so we can always reference it in future for movement up/down
    def drawPaddle(self, board):
        return board.create_rectangle(self.X_COORD, self.yCoord, self.X_COORD+self.WIDTH, self.yCoord+self.HEIGHT, fill=self.FILL_COLOUR)


    def calculateXCoord(self, board, right):
        if right:
            return (board.getBoardWidth() - (board.getPaddleDistanceX()+self.WIDTH))
        else:
            return board.getPaddleDistanceX()

    #####MOVEMENT#####

    def updatePaddle(self, board):
        board.move(self.PADDLE_ID, self.X_COORD ,self.yCoord)

    def up(self):
        self.yCoord -= self.MOVEMENT_DISTANCE

    def down(self):
        self.yCoord += self.MOVEMENT_DISTANCE

    def moveUp(self, board):
        self.up()
        self.collisionDetectionUp(board)
        updatePaddle(board)
            
    def moveDown(self, board):
        self.down()
        self.collisionDetectionDown(board)
        updatePaddle(board)

    def collisionDetectionDown(self, board):
        if self.yCoord > board.getBoardHeight():#going off the bottom of board
            self.resolveBoardCollision(board.getBoardHeight())
        
    def collisionDetectionUp(self, board):
        if self.yCoord < 0:#going off the top of board
            self.resolveBoardCollision(0)

    def resolveBoardCollision(self, correctionValue):
        self.yCoord = correctionValue



    #####GETTERS#####
        
    def getPaddleWidth(self):
        return self.WIDTH

    def getPaddleX(self):
        return self.X_COORD

    def getPaddleBoundingBox(self):
        x0 = self.X_COORD
        y0 = self.yCoord
        x1 = self.X_COORD + self.WIDTH
        y1 = self.yCoord + self.HEIGHT
        return x0, y0, x1, y1

    def getRight(self):
        return self.RIGHT


    #####SETTERS#####


class Ball:
    self.TOTAL_VELOCITY = 100
    def __init__(self, board):
        self.RADIUS = board.getBallRadius()
        self.initialiseBallPosition(board)


    def initialiseBallPosition(self, board):
        self.xCoord = board.getBallPositionX()#returns initial x and y coords of ball
        self.yCoord = board.getBallPositionY()

        launchAngle = math.radians(random.randint(0, 360))
        self.xVelocity = self.TOTAL_VELOCITY * math.cos(launchAngle)
        self.yVelocity = self.TOTAL_VELOCITY * math.sin(launchAngle)

        self.BALL_ID = drawBall(board)
        

    def updatePosition(self):
        self.xCoord = self.xCoord + (self.xVelocity*1) #assuming all frames are equal in length, i.e. t=1
        self.yCoord = self.yCoord + (self.yVelocity*1)

    def checkCollision(self,board, paddle1, paddle2):
        circleLeftX, circleTopY, circleRightX, circleBottomY = self.getCircleBoundingBox()
        paddle1LeftX, paddle1TopY, paddle1RightX, paddle1BottomY = paddle1.getPaddleBoundingBox()
        paddle2LeftX, paddle2TopY, paddle2RightX, paddle2BottomY = paddle2.getPaddleBoundingBox()


        #edge case: what if the circle goes off the top and the right boundaries at the same time?
        #Then the right/left boundary will get priority, and cause a goal as expected
        if circleRightX <0:
            return "right"
        elif circleLeftX > board.getBoardWidth():
            return "left"
        elif circleTopY < 0: #circle off the top of the board
            return "top"
        elif circleBottomY > board.getBoardHeight(): #circle off the bottom of the board
            return "bottom"            


    def resolveBoardCollision(self,board):
        #interpolate the coordinate of the ball post board collision
        pass

    def resolveCollision(self, board, paddle1, paddle2):
        
        
            

        

    def getCircleBoundingBox(self):
        x0 = self.xCoord - self.RADIUS
        y0 = self.yCoord - self.RADIUS
        x1 = self.xCoord + self.RADIUS
        y1 = self.yCoord + self.RADIUS
        return x0, y0, x1, y1

    
    def drawBall(self, board):
        x0, y0, x1, y1 = self.getCircleBoundingBox()        
        return board.create_circle(x0, y0, x1, y1)

    def updateBall(self, board):
        x0, y0, x1, y1 = self.getCircleBoundingBox()
        board.move(self.BALL_ID, x0, y0, x1, y1)

        
        
        
