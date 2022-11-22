import random, sys
from nltk.corpus import wordnet as wn
from SyllableCounter import SyllableCounter
import numpy as np

POETS = ['emerson', 'frost', 'longfellow', 'neruda', 'plath', 'poe', \
        'stowe', 'whitman']

class Poet:
    def __init__(self, filename):
        self.filename = filename
        self.sylco = SyllableCounter()
        self.inspoPoems = {}
        self.numPoems = 0
        self.numStanzas = 0
        self.syllablesPerVerse = 0
        self.versesPerStanza = 0

    def readFile(self):
        """
        Once a Poet object has been created, this method accesses the instance
        variable self.filename, reads the respective file, and extracts the 
        poem contents into self.inspoPoems

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
                self.inspoPoems[currTitle].append(line.rstrip())

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
                        sylls = self.sylco.syllableCounter(word)
                        totalSyllables += sylls

        self.syllablesPerVerse = round(totalSyllables / totalVerses)

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

def main():
    """
    Driver
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
    myPoet.readFile()
    myPoet.computeNumStanzas()
    myPoet.computeSyllablesAndStanzas()
    myPoet.getPoemInfo()

    """
    syns = wn.synsets("program")
    print("Syns: ")
    for i in range(len(syns)-1):
        print(syns[i].lemmas()[0].name())
    """

if __name__ == "__main__":
    main()