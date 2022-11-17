import pickle
import os

studentIDs = ["#1", "#2", "#3", "#4", "#5", "#6"]
studentNames = ["Mokkh", "Daniel", "Kong", "Third", "Gun", "Tim"]
studentAges = [17, 18, 18, 17, 19, 17]
fileName = "sequentialFileAccessRecord.DAT"

class Student:
    def __init__(i, n, a):
        self.studentID = i
        self.name = n
        self.age = a

def createRecord(studentID, name, age):
    s = Student(studentID, name, age)
    return s
    
#create a record to add

#add record to file, search record in file, delete record from file
def addRecord(r):
    with open(fileName, "rb") as f:
        with open("New"+fileName, "wb") as nf:
            loop = True
            while loop:
                try:
                    fileRecord = pickle.load(f)
                    if r.studentID > fileRecord.studentID:
                        currentRecords.append
                    
                    
                except EOFError:
                    loop = False


    dealWithFiles(fileName, "New"+fileName)


def dealWithFiles(a, b):
    os.remove(a)
    os.rename(b, a)
    

def searchRecord(r):
    #with open(fileName, "rb"):
        
        

def deleteRecord(r):
    pass

def main():
    r = createRecord(studentIDs[0], studentNames[1], studentAges[2])
    addRecord(r)
    
    
    
