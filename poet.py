"""
Drew Hofer
November 22, 2022
CSCI 3725, Professor Harmon

The Poet class is designed to generate poetry. Given a filename, Poet extracts
and stores the contents of the inspiring set, computes the characteristics of
the new poem, and generates original poetry following the syntactical structure 
of the inspiring author and other attributes (number of stanzas, number of
verses per stanza, and number of syllables per verse).
"""

import random, sys
from nltk.corpus import wordnet as wn
from SyllableCounter import SyllableCounter
from Tagger import Tagger
from collections import defaultdict
import os
import re

#Globals
POETS = ['emerson', 'frost', 'longfellow', 'neruda', 'plath', 'poe', \
        'stowe', 'whitman']

POETS_REF = {'emerson': 'Ralph Waldo Emerson', 'frost' : 'Robert Frost', \
    'longfellow': 'Henry Wadsworth Longfellow', 'neruda': 'Pablo Neruda', \
        'plath': 'Sylvia Plath', 'poe': 'Edgar Allen Poe', \
            'stowe': 'Harriet Beecher Stowe', 'whitman': 'Walt Whitman'}

RANDOM_SYNSET_PROB = 0.1

STARTING_TYPES = ['NN']

class Poet:
    def __init__(self, filename):
        """Initializer"""
        self.filename = filename
        self.sylCounter = SyllableCounter()
        self.tagger = Tagger()
        self.inspoPoems = {}
        self.numPoems = 0
        self.numStanzas = 0
        self.syllablesPerVerse = 0
        self.preciseSyllablesPerVerse = 0.0
        self.allWords = []
        self.versesPerStanza = 0
        self.corpus = []
        self.taggedData = []
        self.partsDistribution = {}
        self.partsList = {}

    def readFile(self):
        """
        This method accesses the instance variable self.filename, reads the 
        respective file, and extracts the poem contents into self.inspoPoems

        return :: None
        """
        print("Reading file " + self.filename + "…")
        file = open('poems/' + self.filename, 'r')
        currTitle = ''
        for line in file.readlines():
            if line.startswith("Title"):
                self.numPoems += 1 # Counts the number of poems in insiring set
                currTitle = line.rstrip().split(' ', 1)[1]
                self.inspoPoems[currTitle] = []

            elif not line.startswith('#'):
                curr = re.sub("[^\w\d'\s]+",'',line)
                self.inspoPoems[currTitle].append(curr.rstrip())
                self.corpus.append(curr)
                self.allWords.extend(curr)
        
        for item in self.corpus:
            for word in item.split():
                self.allWords.append(word)
        
        #print(self.allWords)

        print("Done reading file " + self.filename + "…")
        file.close()

    def poemsToString(self):
        """
        This method prints out the contents of self.inspoPoems in a
        user-friendly format.

        return :: None
        """
        if self.numPoems == 0:
            print("self.numPoems not yet initialized…")

        else:
            for key, value in self.inspoPoems.items():
                print("Title: " + key)
                for item in value:
                    print(item)

    def computeNumStanzas(self):
        """
        Computes the average number of stanzas in the inspiring poets set and 
        assigns to self.numStanzas. Also computes the average number of verses
        per stanza in the inspiring poets set and assigns to 
        self.versesPerStanza.

        return :: None
        """
        totalStanzas = 0
        verses = 0
        for poem in self.inspoPoems.values():
            for line in poem:
                if line == '':
                    totalStanzas += 1
                else:
                    verses += 1
            totalStanzas += 1

        self.numStanzas = round(totalStanzas / self.numPoems)
        self.versesPerStanza = round(verses / totalStanzas)

    def computeSyllablesAndStanzas(self):
        """
        Computes the average number of syllables per verse in the inspiring 
        poets set and assigns to self.numStanzas

        return :: None
        """
        totalSyllables = 0
        totalVerses = 0

        for poem in self.inspoPoems.values():
            for line in poem:
                if line != '':
                    totalVerses += 1
                    for word in line.split(' '):
                        sylls = self.sylCounter.syllableCounter(word)
                        totalSyllables += sylls

        self.syllablesPerVerse = round(totalSyllables / totalVerses)
        self.preciseSyllablesPerVerse = totalSyllables / totalVerses

    def getPoemInfo(self):
        """
        Prints out the structure of the to be generated poem in a user
        friendly format. 
        
        return :: None
        """
        print("Your poem will be structured in the following way:")
        print("Stanzas: " + str(self.numStanzas))
        print("Syllables per verse: " + str(self.syllablesPerVerse))
        print("Verses per stanza: " + str(self.versesPerStanza))

    def tagData(self):
        """
        Calls the Tagger on every line of the poem in the corpus, so the
        taggedData is now tuples of the form (syntactic category, token)
        
        return :: None
        """
        for line in self.corpus:
            if line != '':
                tagged = self.tagger.getTags(line)
                self.taggedData.append(tagged)

    def compilePartsDistribution(self):
        """
        Accesses the tagged data and creates frequency distribution mapping
        each syntactic category to the syntactic categroies that appear 
        directly after it and how many times. 

        Return :: None

        cfd implentation insipred by Tyler Hallada at:
        https://www.hallada.net/2017/07/11/generating-random-poems-with-python.html
        """
        cfd = defaultdict(lambda: defaultdict(lambda: 0))
        for item in self.taggedData:
            for i in range(len(item) - 2):  # loop to the next-to-last word
                cfd[item[i][1].replace('$', '')][item[i+1][1].replace('$', \
                    '')] += 1  

        dictionary = dict(cfd)
        for key, value in dictionary.items():
            dictionary[key] = dict(value)

        self.partsDistribution = dictionary

    def compilePartsLists(self):
        """
        Accesses the tagged data to make lists of seen words for each 
        syntactic category identified in the training data.  
        
        return :: None
        """
        for item in self.taggedData:
            for i in range(len(item) - 2):
                if item[i][1].replace('$', '') in self.partsList.keys():
                    self.partsList[item[i][1].replace('$', '')].\
                        append(item[i][0])
                else:
                    self.partsList[item[i][1].replace('$', '')] = [item[i][0]]

    def getRandomSyn(self, word):
        """
        word (String) : The word we would like a random synony for

        Takes in a word and, using WordNets synset feature, randomly chooses
        a synonym of the word. A "mutation" of sorts. 

        return :: String — The selected synonym of the input word. 
        """
        syns = wn.synsets(word)
        synSet = set()
        for i in range(len(syns)-1):
            synSet.add(syns[i].lemmas()[0].name())
    
        synSet = list(synSet)
        if len(synSet) > 0:
            return random.choice(synSet)
        else:
            return None

    def getNextWord(self, prevType):
        """
        prevtype (String) - the syntactic category of the previous word

        Given the syntactic category of the previous word, generates the next 
        word in the poem by selecting from the most likely syntactic
        category from the partsDistribution.

        return currType (String) — the syntactic category of the new word
        return newWord (String) — the next word to be put in the poem
        """
        currType = None
        newWord = None
        dist = self.partsDistribution.get(prevType)
        ty = max(dist, key=dist.get)
        newWord = random.choice(self.partsList.get(ty))
        currType = ty
        ran = random.random()
        # Use random synonym with P(RANDOM_SYNSET_PROB)
        if ran < RANDOM_SYNSET_PROB:
            syn = self.getRandomSyn(newWord)
            if syn != None: # if synonym available
                newWord = syn
        return currType, newWord

    def genPoem(self):
        """
        Generates the lines of the new poem according to the previously 
        calculated number of stanzas, verses per stanza, and approximate
        number of syllables per line.
        
        return :: None
        """
        poem = []
        start = random.choice(STARTING_TYPES)
        #print(random.choice(self.partsList.get(start)))
        stanzas = 0
        verses = 0
        while stanzas < self.numStanzas:
            line = []
            syllables = 0
            while verses < self.versesPerStanza + 1:
                while syllables < self.syllablesPerVerse:
                    currType, newWord = self.getNextWord(start)
                    line.append(newWord)
                    start = currType
                    syllables += self.sylCounter.syllableCounter(newWord)
                syllables = 0
                poem.append(line)
                line = []
                verses += 1
            verses = 0
            stanzas += 1

        return poem

    def writePoem(self, poem):
        """
        poem (list) : the line of the generated poem

        Takes the lines of the generated poem and writes them to a .txt file 
        in the output directory. Also calls readAndDisplay() to open the
        generated poem in a .txt file and recite the poem aloud. 

        return :: None
        """
        print("Writing to output file…")
        length = len(self.filename)
        poet = self.filename[:length-4]
        file = open('output/' + poet + ".txt", 'w')
        start = "A poem inspired by the style, structure, and vocabulary of "
        file.write(start + POETS_REF.get(poet) + ":\n\n")
        curr = 0
        for i in range(0, self.versesPerStanza*self.numStanzas):
            curr += 1
            if curr == self.versesPerStanza:
                file.write("\n")
                curr = 0
            else:
                file.write(' '.join(poem[i]) + "\n")

        print("Write complete.")
        file.close()
        self.readAndDisplay(start, poem)

    def readAndDisplay(self, start, poem):
        """
        start (string) : Message to be recited at beginning of poem
        poem (list) : A list of all the lines in the poem

        Uses the OS TTS to recite a psuedo-title for the poem and then speaks
        each line in the poem.
        
        return :: None
        """
        os.system("open output/" + self.filename)
        os.system("say " + start)
        for line in poem:
            os.system("say " + ' '.join(line))

    def getFitness(self, poem):
        """
        poem (list) : The lines of the poem we are going to calculate the 
                      fitness for

        This method determines and prints the fitness of the generated poem 
        by taking the average of two metrics that measure the poems overall
        similarity to the structure of the inspiring poems. 
        1. Average # syllables per verse in generated poem / Average # 
           syllables per verse in inspiring set
        2. (Unique words / total words) *generated* / 
           (Unique words / total words) *inspiring*
        
        return :: None
        """
        genWords = []
        verses = 0
        syllables = 0

        for line in poem:
            for item in line:
                genWords.append(item.rstrip())
                syllables += self.sylCounter.syllableCounter(item.rstrip())
            verses += 1
        
        perVerse = syllables / verses
        syllFitness = perVerse / self.preciseSyllablesPerVerse

        poemWordFitness = (len(set(genWords)) / len(genWords))
        inspoWordFitness = len(set(self.allWords)) / len(self.allWords)
        wordFitness = poemWordFitness / inspoWordFitness
        overallFitness = (syllFitness + wordFitness) / 2
        print("The overall fitness of this poem is: " + str(overallFitness))

def main():
    """
    The driver of the entire program. Extracts file, creates a Poet object, 
    and performs the necessary steps for poem generation. 
    """
    poet = None
    if len(sys.argv) == 2 and sys.argv[1] in POETS:
        poet = sys.argv[1]
    else:
        print("Invalid poet. Selecting poet randomly…")
        poet = random.choice(POETS)

    print("Poet is " + poet + ".")
    filename = poet + '.txt'

    myPoet = Poet(filename)
    print(myPoet.getRandomSyn('table'))
    myPoet.readFile()
    myPoet.computeNumStanzas()
    myPoet.computeSyllablesAndStanzas()
    myPoet.getPoemInfo()
    myPoet.tagData()
    myPoet.compilePartsDistribution()
    myPoet.compilePartsLists()
    poemLines = myPoet.genPoem()
    myPoet.getFitness(poemLines)
    myPoet.writePoem(poemLines)
    myPoet.getFitness(poemLines)

if __name__ == "__main__":
    main()