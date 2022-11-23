The Edgar Allen Poem Generator\
Drew Hofer\
November 22, 2022\
CSCI 3725, Professor Harmon\

The Edgar Allen Poem Generator generates poetry based on the specified poet, 
or randomly selects one if an invalid one is given. To specify a poet, run the
program from the poetry-slam directory on the command line in the following way:

python3 poet.py poet

where valid poets are 'emerson', 'frost', 'longfellow', 'neruda', 'plath', 
'poe', 'stowe', 'whitman'

The poet.py then performs the following:

Read in the specified inspiring set\
– {Poem Title : [Lines of poem], ... }\
Create corpus: [Every line from inspiring set]\
Compute poem structure based on the inspiring set\
– Average number of stanzas per poem\
– Average number of verses per stanza\
– Average number of syllables per stanza\
Tag corpus, creating a syntax tree for every line in the inspiring set\
Compile tagged data\
– First-order Markov chain used to determine the syntactic category of the next word\
– Category lists — {Syntactic category : [words in that category], ... }\

External Sources Used:\
Syntax Tree in Python from samishawl at: https://www.geeksforgeeks.org/syntax-tree-natural-language-processing/

Counting Syllables in the English Language Using Python at: https://eayd.in/?p=232

cfd implentation from Tyler Hallada at:
https://www.hallada.net/2017/07/11/generating-random-poems-with-python.html

Challenges:\
I was challenged as a computer scientist in this project in a number of ways, 
most greatly by the task of mimicking human intelligence and creativity. There
are so many aspects of poetry that are quite complicated and beyond the 
understanding of a simple machine. One thing that I find interesting about 
poetry is form. The length of lines, number of syllables, and connections
between words is an art. But, since it's an art, it's also a great challenge 
to attempt to make a machine understand it. 

I was also challenged by working with different libraries I had no prior
experience with. While testy and frustrating at times, it's rewarding to learn
something new and then see it in practice. 

Inspirations:\
Hugo Gonçalo Oliveira (https://aclanthology.org/W17-3502/) for the idea to
really hone in on the semantics and structure of poetry

Toivanen, Jukka et al. (https://helda.helsinki.fi/handle/10138/37269) for the 
corpus based generation model

Ron Bekkerman et al. (https://cs.brynmawr.edu/Courses/cs380/fall2006/ir-408.pdf)
for the bigram apprach to syntactical structure
