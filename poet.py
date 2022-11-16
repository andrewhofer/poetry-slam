import random, sys
import numpy as np

POETS = ['emerson', 'frost', 'longfellow', 'neruda', 'plath', 'poe', \
        'stowe', 'whitman']

class Poet:
    def __init__(self, filename):
        self.filename = filename
        self.inspoPoems = {}
        self.numPoems = 0

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
        user-friendly format

        return :: None
        """
        if self.numPoems == 0:
            print("self.numPoems not yet initialized…")

        else:
            for key, value in self.inspoPoems.items():
                print("Title: " + key)
                for item in value:
                    print(item)

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
    myPoet.poemsToString()


if __name__ == "__main__":
    main()