# Python program for insert and search
# operation in a Trie
# import pickle


def read_dictionary(dictionary_file=None):

    dictionary_file = 'male_and_female_names.txt' if dictionary_file == None else dictionary_file
    with open(dictionary_file, 'r') as f:
        file = f.readlines()
        data = [word.strip().replace(' ', '') for word in file]
        return data


def prepair_word(word=''):

    # Remove tonos
    without_tonos = ['α', 'ε', 'η', 'ι', 'ο', 'υ', 'ω', 'ι']
    with_tonos = ['ά', 'έ', 'ή', 'ί', 'ό', 'ύ', 'ώ', 'ϊ']

    for letter_index, letter in enumerate(with_tonos):
        try:
            word_index = word.index(letter)
        except ValueError:
            next
        else:
            word = word.replace(
                word[word_index], without_tonos[letter_index])

    return word.lower()


class TrieNode:

    # Trie node class
    def __init__(self):
        self.children = [None]*26

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False


class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def _charToIndex(self, ch):

        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
        return ord(ch)-ord('α')

    def insert(self, key):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # mark last node as leaf
        pCrawl.isEndOfWord = True

    def search(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl != None and pCrawl.isEndOfWord


def identify(dataset=None, testwords=[]):
    # data = './male_and_female_names.txt' if data == None else data
    # with open(data) as f:
    #     data = f.read().replace('\n', '').lower()

    output = ["Not present in trie",
              "Present in trie"]
    dataset = 'male_and_female_names.txt' if dataset == None else dataset
    data = read_dictionary(dictionary_file=dataset)
    # Input words (prepaired to only 'α' through 'ω' and lower case)
    dictionary = [prepair_word(word) for word in data]
    # Trie object
    t = Trie()

    # Construct trie
    for word in dictionary:
        t.insert(word)
    # Possible names. Words that start with uppercase letter
    possible_names = []
    name_found = []
    for word in testwords:
        # Search for different keys
        # print("{} ---- {}".format(word,
        #                           output[t.search(prepair_word(word=word))]))
        if t.search(prepair_word(word=word)) == 1:
            #word is found
            name_found.append(True)
        else:
            name_found.append(False)
    return name_found
