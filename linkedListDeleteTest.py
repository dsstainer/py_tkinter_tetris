myLinkedList = [27, 19, 36, 42, 16, None, None, None, None, None, None, None]
myLinkedListPointers = [-1, 0, 1, 2, 3, 6, 7, 8, 9, 10, 11, -1]
startPointer = 4
nullPointer = -1
heapStartPointer = 5

def delete(itemDelete):
    global startPointer, heapStartPointer
    if startPointer == -1:
        print("Linked list empty")
    else:
        index = startPointer
        while myLinkedList[index] != itemDelete and index != -1:
            oldindex = index
            index = myLinkedListPointers[index]
        if index == -1:
            print("Item", itemDelete, "not found")
        else:
            myLinkedList[index] = None
            tempPointer = myLinkedListPointers[index]
            myLinkedListPointers[index] = heapStartPointer
            heapStartPointer = index
            myLinkedListPointers[oldindex] = tempPointer


print("Before:\n",myLinkedList)
print(myLinkedListPointers)
print(startPointer)
delete(16)
print("After:\n",myLinkedList)
print(myLinkedListPointers)
print(startPointer)
