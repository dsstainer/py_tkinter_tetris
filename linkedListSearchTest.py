myLinkedList = [27, 19, 36, 42, 16, None, None, None, None, None, None, None]
myLinkedListPointers = [-1, 0, 1, 2, 3, 6, 7, 8, 9, 10, 11, -1]
startPointer = 4
nullPointer = -1
def find(itemSearch):
    found = False
    itemPointer = startPointer
    while itemPointer != -1 and not found:
        if myLinkedList[itemPointer] == itemSearch:
            found = True
        else:
            itemPointer = myLinkedListPointers[itemPointer]
    return itemPointer

item = 27
result = find(item)
if result != -1:
    print("Item found at,", result)
else:
    print("Item not found")
