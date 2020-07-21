class Trie:
    def __init__(self):
        self.root = Node("!")

    def insert(self, word):
        node = self.root
        for i in range(len(word)):
            if node.links[ord(word[i]) - 97] == None:
                node.links[ord(word[i]) - 97] = Node(word[i])
            node = node.links[ord(word[i]) - 97]
        if node.links[26] != None and node.links[26].count > 1:
            node.links[26].count += 1
        else:
            node.links[26] = Node("$")
            node.links[26].word = word
            node.links[26].count = 1

    def search(self,word):
        node = self.root

        for i in range(len(word)):
            if node.links[ord(word[i]) - 97] == None:
                return False

            if word[i] != node.links[ord(word[i]) - 97].data:
                return False

            node = node.links[ord(word[i]) - 97]
            if i == len(word) - 1:
                if node.links[26] != None and node.links[26].data == "$":
                    return True
                return False


    #auto-complete
    def inorder(self, word):
        node = self.root
        for i in range(len(word)):
            if node.links[ord(word[i]) - 97] == None:
                return "String not found"
            node = node.links[ord(word[i]) - 97]
        if node.links[-1] != None:
            return [node.links[-1].word, node.links[-1].count]
        else:
            return self.inorder_aux(node)

    def inorder_aux(self, current):
        wordList = []
        if current.links[-1] != None:
            wordList.append([current.links[-1].word, current.links[-1].count])
        for i in range(len(current.links) - 1):
            if current.links[i] is not None:

                result = self.inorder_aux(current.links[i])
                for j in range(len(result)):
                    wordList.append(result[j])


        return wordList


class Node:
    def __init__(self,data):
        self.data = data
        self.word = ""
        self.links = [None]*27
        self.count = 0



if __name__ == "__main__":
    t = Trie()
    t.insert("lionel")
    t.insert("lion")
    t.insert("lol")
    t.insert("bbb")
    t.insert("bb")

    print(t.inorder("l"))
