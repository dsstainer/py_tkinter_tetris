class Node:
    def __init__(self):
        self.leftPtr = -1
        self.rightPtr = -1
        self.data = ""

class BinaryTree:
    def __init__(self, size):
        self.size = size
        self.b = [Node() for x in range(size)]
        self.rootPtr = -1
        self.freePtr = 0
        self.linkFreeList()

    def linkFreeList(self):
        for x in range(self.size-1):
            self.b[x].leftPtr = x+1

    def display(self):
        for index,n in enumerate(self.b):
            print(index,n.leftPtr, n.data ,n.rightPtr)

    def insertElement(self, item):
        if self.freePtr != -1:#not full
            entryIndex = self.freePtr #enter at the next free index
            self.freePtr = self.b[entryIndex].leftPtr #next item in freeList
            self.b[entryIndex].data = item
            self.b[entryIndex].leftPtr = -1 #new items always point to null
            

            #place item logically by changing pointers of previous items
            if self.rootPtr == -1:#first item in tree
                self.rootPtr = entryIndex
            else:
                loop = True
                currentIndex = self.rootPtr
                while loop:
                    if item >= self.b[currentIndex].data:#equal items go to the right
                        if self.b[currentIndex].rightPtr == -1:#if there is a space,
                            self.b[currentIndex].rightPtr = entryIndex#add the item
                            loop = False
                        else:
                            currentIndex = self.b[currentIndex].rightPtr
                            
                    else:#small items go to left
                        if self.b[currentIndex].leftPtr == -1:
                            self.b[currentIndex].leftPtr = entryIndex
                            loop = False
                        else:
                            currentIndex = self.b[currentIndex].leftPtr

            """
            Alternatively for looping part
            
                right = True
                previousIndex = -1
                currentIndex = self.rootPtr
                while currentIndex != -1:
                    previousIndex = currentIndex
                    if item >= self.b[currentIndex].data:#equal items go to the right
                            currentIndex = self.b[currentIndex].rightPtr
                            right = True
                            
                    else:#small items go to left
                            currentIndex = self.b[currentIndex].leftPtr
                            right = False
                if right:
                    self.b[previousIndex].rightPointer = entryIndex
                else:
                    self.b[previousIndex].leftPointer = entryIndex



            
            """

    def searchElement(self, item):
        if self.rootPtr != -1:
            currentIndex = self.rootPtr
            found = False
            while currentIndex != -1 and not found:
                if self.b[currentIndex].data == item:
                    print("Item found at index:", currentIndex)
                    found = True
                elif item > self.b[currentIndex].data:
                    currentIndex = self.b[currentIndex].rightPtr
                else:
                    currentIndex = self.b[currentIndex].leftPtr
            if not found:
                print("Item not in list")


    
    def inOrderTraversalR(self, currentIndex):
        if currentIndex != -1:
            self.inOrderTraversalR(self.b[currentIndex].leftPtr)
            print(self.b[currentIndex].data)
            self.inOrderTraversalR(self.b[currentIndex].rightPtr)
        """
        Alternatively
        
        if self.b[currentIndex].leftPtr != -1:
            self.postOrderTraversal(self.b[currentIndex].leftPtr)

        print(self.b[currentIndex].data)

            
        if self.b[currentIndex].rightPtr != -1:
            self.postOrderTraversal(self.b[currentIndex].rightPtr)

        """

            

    def inOrderTraversal(self):
        self.inOrderTraversalR(0)
        



     
            
            


b = BinaryTree(5)
b.insertElement("Mokkh")
b.insertElement("Daniel")
b.insertElement("Mr.V")
b.insertElement("Fat")
b.display()
b.inOrderTraversal()
                            
                
                    
                        
                    
            




            
