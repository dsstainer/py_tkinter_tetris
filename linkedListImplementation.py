class Node:
    def __init__(self):
        self.item = ""
        self.pointer = -1

class OrderedLinkedList:
    def __init__(self,size):
        self.linkedListSize = size
        self.linkedList = [Node() for x in range(self.linkedListSize)]
        self.headPointer = -1
        self.freePointer = 0
        for i in range(self.linkedListSize-1):
            self.linkedList[i].pointer = i+1        


    def isFull(self):
        return self.freePointer == -1


    def isEmpty(self):
        return self.headPointer == -1

    def searchElement(self,item):
        currentPtr = self.headPointer
        while self.linkedList[currentPtr].item <= item and currentPtr != -1:
            if self.linkedList[currentPtr].item == item:
                return ("Item found at index " + str(currentPtr)+"\n")
            currentPtr = self.linkedList[currentPtr].pointer
        return "Not found\n"

    def deleteElement(self,item):
        if self.isEmpty():
            print("Linked list is empty, no items can be deleted")
        else:
            previousPtr = -1
            currentPtr = self.headPointer
            while self.linkedList[currentPtr].item != item and currentPtr != -1 and self.linkedList[currentPtr].item < item:
                previousPtr = currentPtr
                currentPtr = self.linkedList[currentPtr].pointer
            if currentPtr == -1 or self.linkedList[currentPtr].item > item:
                print( "Item not in linked list")
            else:#linkedList[currentPtr] == item
                if previousPtr == -1:#we remove first item in list
                    self.headPointer = self.linkedList[currentPtr].pointer
                else:
                    self.linkedList[previousPtr].pointer = self.linkedList[currentPtr].pointer#remove item logically
                    
                self.linkedList[currentPtr].item = ""
                self.linkedList[currentPtr].pointer = self.freePointer
                self.freePointer = currentPtr

    def insertElement(self, item):
        if self.isFull():
            print("Linked list is full, no items can be inserted")
        else:
            itemPosition = self.freePointer
            self.linkedList[itemPosition].item = item #Add item to freeList
            self.freePointer = self.linkedList[itemPosition].pointer #update freePointer
            if self.isEmpty(): #check whether this is the first item to be added
                self.headPointer = itemPosition
                self.linkedList[itemPosition].pointer = -1
            else:
                if item < self.linkedList[self.headPointer].item:#check whether this should be first item. We treat this seperately cause we mess around with headPointer
                    self.linkedList[itemPosition].pointer = self.headPointer #update pointer of insert item
                    self.headPointer = itemPosition #update headPointer
                else:
                #find where we should insert the item --> traverse
                    previousPtr = -1
                    currentPtr = self.headPointer
                    while currentPtr != -1 and item >= self.linkedList[currentPtr].item:
                        previousPtr = currentPtr
                        currentPtr = self.linkedList[currentPtr].pointer
                        
                    temp = self.linkedList[previousPtr].pointer
                    self.linkedList[previousPtr].pointer = itemPosition
                    self.linkedList[itemPosition].pointer = temp

    def traverseList(self):
        currentPtr = self.headPointer
        while currentPtr != -1:
            x = self.linkedList[currentPtr]
            print("(",x.item,",", x.pointer,")" ,end="")
            currentPtr = x.pointer
        print("\n")

    def display(self):
        for index, x in enumerate(self.linkedList):
            print(index, x.item, x.pointer)
        print("///////////////////////////////////////////////////////")






        
    









        
        
