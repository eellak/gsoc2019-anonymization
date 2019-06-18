# Python program for insert and search
# operation in a Trie
# import pickle


def read_dictionary(dictionary_file=None):

    dictionary_file = 'male_and_female_names.txt' if dictionary_file == None else dictionary_file
    with open(dictionary_file, 'r') as f:
        file = f.readlines()
        data = [prepair_word(word.strip().replace(' ', ''))
                for word in file]
        return data


def prepair_word(word=''):

    # Lowercase word
    word = word.lower()

    # Remove tonos
    without_tonos = ['α', 'ε', 'η', 'η', 'ι', 'ι', 'ι', 'ι',
                     'ο', 'υ', 'υ', 'υ', 'υ', 'ω',  'ω']

    with_tonos = ['ά', 'έ', 'ή', 'ἡ', 'ί', 'ἰ', 'ϊ', 'ΐ',
                  'ό', 'ύ', 'ϋ', 'ῦ', 'ῦ', 'ώ', 'ῶ']

    for letter_index, letter in enumerate(with_tonos):
        try:
            word_index = word.index(letter)
        except ValueError:
            next
        else:
            word = word.replace(
                word[word_index], without_tonos[letter_index])

    return word


def read_dictionary(dictionary_file=None):

    dictionary_file = 'male_and_female_names.txt' if dictionary_file == None else dictionary_file
    with open(dictionary_file, 'r') as f:
        file = f.readlines()
        data = [prepair_word(word.strip().replace(' ', ''))
                for word in file]
        return data


class TrieNode:

    # Trie node class
    def __init__(self):
        self.children = [None]*28

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False


class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def _charToIndex(self, ch, print_index=False):

        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
        if print_index == True:
            print(f'ord(ch)={ord(ch)}')
        # Special characters added
        # Catching: <.>,<_>,<\r> (for windows)

        if ch == '.':
            return 26
        if ch == '_':
            return 25
        if ord(ch) == 10:
            return 27
        if ord(ch) - ord('α') > 24 or ord(ch) - ord('α') < 0:
            exit(
                f'''Error at _charToIndex while searching trie index: ord(ch)={ord(ch)}''')
        return ord(ch)-ord('α')

    def insert(self, key):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if ord(key[level]) == 10:
                continue
            if index > 26 or index < 0:
                exit(
                    f'''Error while inserting:
                        key: {key}
                        character level: {level}
                        character: {key[level]}
                        Index trying to access: {index}
                        ord(character): {ord(key[level])}
                    ''')

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # mark last node as leaf
        pCrawl.isEndOfWord = True

    def search(self, key, print_index=False):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level], print_index=print_index)
            if print_index == True:
                print(index)
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        return pCrawl != None and pCrawl.isEndOfWord


def create_trie_index_for_names(dataset=None):

    dataset = 'anonymizer/data/male_and_female_names.txt' if dataset == None else dataset
    data = read_dictionary(dictionary_file=dataset)
    # Input words (prepaired to only 'α' through 'ω' and lower case)
    dictionary = [word for word in data]
    # Trie object
    t = Trie()

    # Construct trie
    for word in dictionary:
        try:
            t.insert(word)
        except:
            from termcolor import colored as color
            print(color(
                  'The following name can not be included in the search:{} from the file: {}'.format(
                      word, dataset),
                  'red'))

    return t


def create_trie_index(dataset=None):

    if dataset == None:
        raise NameError('No dataset given for trie index to be initialized.')

    with open(dataset, mode='r') as f:
        file = f.readlines()
        data = [word.replace('\r', '\n').replace(
            '\u000D\u000A', '\n').replace('(', '\n').replace(')', '\n') for word in file]

    t = Trie()

    for word in data:
        try:
            word = prepair_word(word.replace(' ', '_').replace(
                '-', '_').replace('\r', '').replace(
                '\u000D\u000A', '\n').replace('\u000D', '\n'))
        # replace spaces with _ and - with _
            t.insert(word)

        except:
            from termcolor import colored as color
            print(color(
                'The following place can not be included in the search:{} from the file: {}'.format(
                    word, dataset),
                'red'))
    return t
