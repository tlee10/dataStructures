class MaxHeap:
    def __init__(self):
        self.heap = []
        self.count = 0

    def root(self):
        return self.heap[0]

    def rise(self, index):

        while (index-1)//2 >= 0 and (self.heap[index] > self.heap[(index-1)//2]):
            tmp = self.heap[index]
            self.heap[index] = self.heap[(index - 1)//2]
            self.heap[(index - 1) // 2] = tmp
            if index % 2 != 0:
                index //= 2
            else:
                index = (index - 1)//2

    def push(self, item):

        self.heap.append(item)
        self.count += 1
        if self.count > 1:
            self.rise(self.count-1)

    def maxChild(self, index):

        if (index * 2) + 2 <= self.count - 1:
            if self.heap[(index * 2) + 2] > self.heap[(index * 2) + 1]:
                return (index * 2) + 2

        return (index * 2) + 1

    def childExists(self, index):
        if (index * 2) + 1 <= self.count-1:
            return True

    def sink(self, index):
        while self.childExists(index) and self.heap[self.maxChild(index)] > self.heap[index]:
            maxIndex = self.maxChild(index)
            tmp = self.heap[index]
            self.heap[index] = self.heap[maxIndex]
            self.heap[maxIndex] = tmp
            index = maxIndex

    def delete(self):
        if self.count == 0:
            raise Exception("Heap is empty")
        elif self.count == 1:
            min = self.heap.pop()
            self.count = 0
        else:
            self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
            min = self.heap.pop()
            self.count -= 1
            self.sink(0)
        return min

    def __len__(self):
        return self.count

    def __str__(self):
        """
            Return the item in the list in string form by concatenating every items to empty string.
               :param :
               :pre-condition
               :post-condition:
               :Complexity - best case(O(n))    bestCase and worstCase are the same because they are both dependent on length of list (n)
                             worst case(O(n))
               :return: return a string that consists of items in the list where every item is in different line.
               """
        strItem = ""
        for i in range(len(self)):
            if i == len(self) - 1:  # to ensure no \n at the end
                strItem += str(self.heap[i])
            else:
                strItem += str(self.heap[i]) + "\n"
        return strItem

    def heapSort(self):
        sortedList = []
        for i in range(len(self)):
            item = self.delete()
            sortedList.append(item)
        return sortedList

if __name__ == "__main__":
    heap = MaxHeap()
    
