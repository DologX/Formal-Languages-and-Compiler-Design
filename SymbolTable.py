class SymbolTable:

    def __init__(self):
        self.hashTable = [[] for _ in range(100)]

    # Display Symbol Table
    def display(self):
        for i in range(len(self.hashTable)):
            print(i, end=" ")
            for j in self.hashTable[i]:
                print("-->", end=" ")
                print(j, end=" ")
            print()

    # Return key for every data
    def __hashing(self, data):
        key = sum(bytearray(data.encode('ASCII')))
        return key % len(self.hashTable)

    # Add values to the hash table
    def add(self, data):
        hashKey = self.__hashing(data)

        if data not in self.hashTable[hashKey]:
            self.hashTable[hashKey].append(data)
            return hashKey, self.hashTable[hashKey].index(data)

        return -1, -1

    # Search for values into hash table
    def search(self, data):
        hashKey = self.__hashing(data)

        if data in self.hashTable[hashKey]:
            return hashKey, self.hashTable[hashKey].index(data)

        return -1, -1

    # Retrieve values from the hash table
    def get(self, position):
        return self.hashTable[position[0]][position[1]]
