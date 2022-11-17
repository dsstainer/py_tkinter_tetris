class Node:
    def __init__(self):
        self.item = ""
        self.pointer = -1



def setUpLinkedList():
    linkedListSize = 10
    linkedList = [Node() for x in range(linkedListSize)]
    headPointer = -1
    freePointer = 0
    for i in range(linkedListSize-1):
        linkedList[i].pointer = i+1
    return linkedListSize, linkedList, headPointer, freePointer

def isFull(freePointer):
    return freePointer == -1

def isEmpty(headPointer):
    return headPointer == -1
    

def insertItem(item, linkedListSize, linkedList, headPointer, freePointer):
    if isFull(freePointer):
        print("Linked list is full, no items can be inserted")
    else:
        itemPosition = freePointer
        linkedList[itemPosition].item = item #Add item to freeList
        freePointer = linkedList[itemPosition].pointer #update freePointer
        if headPointer == -1: #check whether this is the first item to be added
            headPointer = itemPosition
            linkedList[itemPosition].pointer = -1
        else:
            if item < linkedList[headPointer].item:#check whether this should be first item. We treat this seperately cause we mess around with headPointer
                linkedList[itemPosition].pointer = headPointer #update pointer of insert item
                headPointer = itemPosition #update headPointer
            else:
            #find where we should insert the item --> traverse
                previousPtr = -1
                currentPtr = headPointer
                while currentPtr != -1 and item >= linkedList[currentPtr].item:
                    previousPtr = currentPtr
                    currentPtr = linkedList[currentPtr].pointer
                    
                temp = linkedList[previousPtr].pointer
                linkedList[previousPtr].pointer = itemPosition
                linkedList[itemPosition].pointer = temp

    return linkedListSize, linkedList, headPointer, freePointer


def display(linkedList):
    for index, x in enumerate(linkedList):
        print(index, x.item, x.pointer)
    print("///////////////////////////////////////////////////////")
        
def traverse(headPointer, linkedList):
    currentPtr = headPointer
    while currentPtr != -1:
        x = linkedList[currentPtr]
        print("(",x.item,",", x.pointer,")" ,end="")
        currentPtr = x.pointer
    print("\n")
    
def searchItem(item,linkedListSize, linkedList, headPointer, freePointer):
    currentPtr = headPointer
    while linkedList[currentPtr].item <= item and currentPtr != -1:
        if linkedList[currentPtr].item == item:
            return ("Item found at index " + str(currentPtr))
        currentPtr = linkedList[currentPtr].pointer
    return "Not found"


def deleteItem(item, linkedListSize, linkedList, headPointer, freePointer):
    if isEmpty(headPointer):
        print("Linked list is empty, no items can be deleted")
    else:
        previousPtr = -1
        currentPtr = headPointer
        while linkedList[currentPtr].item != item and currentPtr != -1 and linkedList[currentPtr].item < item:
            previousPtr = currentPtr
            currentPtr = linkedList[currentPtr].pointer
        if currentPtr == -1 or linkedList[currentPtr].item > item:
            print( "Item not in linked list")
        else:#linkedList[currentPtr] == item
            if previousPtr == -1:#we remove first item in list
                headPointer = linkedList[currentPtr].pointer
            else:
                linkedList[previousPtr].pointer = linkedList[currentPtr].pointer#remove item logically
                
            linkedList[currentPtr].item = ""
            linkedList[currentPtr].pointer = freePointer
            freePointer = currentPtr

    return linkedListSize, linkedList, headPointer, freePointer

def main():
    linkedListSize, linkedList, headPointer, freePointer = setUpLinkedList()
    display(linkedList)
    traverse(headPointer, linkedList)
    
    linkedListSize, linkedList, headPointer, freePointer =insertItem("Mokkh", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer =insertItem("Luke", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer =insertItem("Kong", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer =insertItem("Daniel", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    print(searchItem("Daniel", linkedListSize, linkedList, headPointer, freePointer))
    print(searchItem("Prim", linkedListSize, linkedList, headPointer, freePointer))
    print(searchItem("Khim", linkedListSize, linkedList, headPointer, freePointer))
    print(searchItem("Jimmy", linkedListSize, linkedList, headPointer, freePointer))
    print(searchItem("Mokkh", linkedListSize, linkedList, headPointer, freePointer))
    print()

    linkedListSize, linkedList, headPointer, freePointer = deleteItem("Daniel", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer = deleteItem("Xi", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer = deleteItem("Kong", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer = insertItem("Luke", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

    linkedListSize, linkedList, headPointer, freePointer = insertItem("Kong", linkedListSize, linkedList, headPointer, freePointer)
    display(linkedList)
    traverse(headPointer, linkedList)

main()
