#! /usr/bin/python
# terse version of huffman10.py - reads counts from stdin       (c) David MacKay  Dec 2005
# - writes a huffman code                              This is Free Software. License: GPL
## For license statement see  http://www.gnu.org/copyleft/gpl.html
"""
The Huffman3 package provides a Huffman algorithm, spitting out 
an optimal binary symbol code for a given set of probabilities.
It also returns two objects that can be used for Encoding
and Decoding with the functions encode and decode.
The two objects are
    - a list of "nodes", one for each symbol;
       this list is used for encoding; and
    - a tree of "internalnodes", accessed via the root
       of the tree, used for decoding.

The package can be used in many ways.
If you just want to quickly find the Huffman code for a set of
relative frequencies, you can run Huffman3.py from a shell like this:

~/python/compression/huffman$ python Huffman3.py 
Reading in frequencies (and optional symbol names) from stdin
50    <<<|
25    <<<| These four lines are the user's input, terminated by Control-D
12    <<<|
13    <<<|
#Symbol Count   Codeword
1       (50)    1
2       (25)    01
3       (12)    000
4       (13)    001

Alternatively, a slightly fancier usage includes symbol names in each line of stdin:

~/python/compression/huffman$ echo -e " 50 a \n 25 b \n 12 c \n 13 d" > ExampleCounts
~/python/compression/huffman$ python Huffman3.py < ExampleCounts 
Reading in frequencies (and optional symbol names) from stdin
#Symbol Count   Codeword
a       (50)    1
b       (25)    01
c       (12)    000
d       (13)    001

Functions supplied by the package:

 iterate(code) runs the Huffman algorithm on a list of "nodes".
          It returns a pointer to the root of a new tree of "internalnodes".

 encode(sourcelist,code) encodes a list os source symbols.

 decode(string,root) decodes a binary string into a list.

 huffman(counts):     Takes in a list of counts.
    Runs the huffman algorithm 'iterate', and optionally sorts and prints the resulting tree.
    
 makenodes(probs):    Creates a list of nodes ready for the Huffman algorithm 'iterate'.
    probs should be a list of pairs('<symbol>', <value>).

Examples illustrating use of this package:

 easytest(): simple example of making a code, encoding and decoding

 oldtest(): this is run when the program is run from a shell.

See also the file Example.py for a python program that uses this package.
"""
import sys, string
class node:
    def __init__(self, count, index , name="" ):
        self.count = float(count)
        self.index = index
        self.name  = name ## optional argument
        if self.name=="" : self.name = index
        self.word = "" ## codeword will go here
        self.isinternal = 0
    def __cmp__(self, other):
        return cmp(self.count, other.count)
    def report(self):
        if (self.index == 1 ) :
            print '#Symbol\tCount\tCodeword'
        print '%s\t(%2.2g)\t%s' % (self.name,self.count,self.word)
        pass
    def associate(self,internalnode):
        self.internalnode = internalnode
        internalnode.leaf = 1
        internalnode.name = self.name
        pass

class internalnode:
    def __init__(self):
        self.leaf = 0
        self.child = []
        pass
    def children(self,child0,child1):
        self.leaf = 0
        self.child.append(child0)
        self.child.append(child1)
        pass
        
def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item

def iterate (c) :
    """
    Run the Huffman algorithm on the list of "nodes" c.
    The list of nodes c is destroyed as we go, then recreated.
    Codewords 'co.word' are assigned to each node during the recreation of the list.
    The order of the recreated list may well be different.
    Use the list c for encoding.

    The root of a new tree of "internalnodes" is returned.
    This root should be used when decoding.

    >>> c = [ node(0.5,1,'a'),  \
              node(0.25,2,'b'), \
              node(0.125,3,'c'),\
              node(0.125,4,'d') ]   # my doctest query has been resolved
    >>> root = iterate(c)           # "iterate(c)" returns a node, not nothing, and doctest cares!
    >>> reportcode(c)               # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    #Symbol   Count	Codeword
    a         (0.5)	1
    b         (0.25)	01
    c         (0.12)	000
    d         (0.12)	001
    """
    if ( len(c) > 1 ) :
        c.sort() ## sort the nodes by count, using the __cmp__ function defined in the node class
        deletednode = c[0] ## keep copy of smallest node so that we can put it back in later
        second = c[1].index ## index of second smallest node
        # MERGE THE BOTTOM TWO
        c[1].count += c[0].count  ##  this merged node retains the name of the bigger leaf.
        del c[0]

	root = iterate ( c )

        ## Fill in the new information in the ENCODING list, c
        ## find the codeword that has been split/joined at this step
        co = find( lambda p: p.index == second , c )
        deletednode.word = co.word+'0'
        c.append( deletednode )  ## smaller one gets 0
        co.word += '1'
        co.count -= deletednode.count   ## restore correct count

        ## make the new branches in the DECODING tree
        newnode0 = internalnode()
        newnode1 = internalnode()
        treenode = co.internalnode # find the node that got two children
        treenode.children(newnode0,newnode1)
        deletednode.associate(newnode0)
        co.associate(newnode1)
        pass
    else :
        c[0].word = ""
        root = internalnode()
        c[0].associate(root)
        pass
    return root

def encode(sourcelist,code):
    """
    Takes a list of source symbols. Returns a binary string.
    """
    answer = ""
    for s in sourcelist:
        co = find(lambda p: p.name == s, code)
        if ( not co  ):
            import sys
            print >> sys.stderr, "Warning: symbol",`s`,"has no encoding!"
            pass
        else:
            answer = answer + co.word
            pass
    return answer

def decode(string,root):
    """
    Decodes a binary string using the Huffman tree accessed via root
    """
    ## split the string into a list
    ## then copy the elements of the list one by one.
    answer = []
    clist = list( string )
    ## start from root
    currentnode = root
    for c in clist:
        if ( c=='\n' ):  continue ## special case for newline characters
        assert ( c == '0' )or( c == '1')
        currentnode = currentnode.child[int(c)]
        if currentnode.leaf != 0:
            answer.append( str(currentnode.name) )
            currentnode = root
        pass
    assert (currentnode == root) ## if this is not true then we have run out of characters and are half-way through a codeword
    return answer

## alternate way of calling huffman with a list of counts ## for use as package by other programs ######
## two example ways of using it:
#>>> from Huffman3 import *
#>>> huffman([1, 2, 3, 4],1)
#>>> (c,root) = huffman([1, 2, 3, 4])

def huffman( counts , verbose=0 ) :
    """
    Takes in a list of counts.
    Runs the huffman algorithm, and optionally sorts and prints the resulting tree.

    >>> c = huffman([0.5, 0.25, 0.125, 0.125],1)          # doctest: +NORMALIZE_WHITESPACE
    #Symbol Count   Codeword
    1       (0.5)   1
    2       (0.25)  01
    3       (0.12)  000
    4       (0.12)  001
    """
    c=[] ## array of nodes
    m=0
    for value in counts : 
        m += 1 ;  c.append( node( value, m ) )
    root = iterate ( c )  # make huffman code
    if (verbose) :
        reportcode(c)
    return (c,root)
## end ##########################################################################

def makenodes(probs):
    """
    Creates a list of nodes ready for the Huffman algorithm.
    Each node will receive a codeword when Huffman algorithm "iterate" runs.

    probs should be a list of pairs('<symbol>', <value>).

    >>> probs=[('a',0.5), ('b',0.25), ('c',0.125), ('d',0.125)]
    >>> symbols = makenodes(probs) 
    >>> root = iterate(symbols) 
    >>> zipped = encode(['a','a','b','a','c','b','c','d'], symbols) 
    >>> print zipped 
    1101100001000001
    >>> print decode( zipped, root ) 
    ['a', 'a', 'b', 'a', 'c', 'b', 'c', 'd']

    See also the file Example.py for a python program that uses this package.
    """
    m=0
    c=[]
    for p in probs:
        m += 1 ;
        c.append( node( p[1], m, p[0] ) )
        pass
    return c

def reportLH(c,verbose=1):
    from  math import log
    total=0;     H=0 ; L=0
    for co in c :                             
        total += co.count
    for co in c :                             
        p = co.count * 1.0 / total
        logp = log(p)/log(2.0)
        H -= p * logp
        L += p * len(co.word)
    if verbose: print "#L = %10.6g    H = %10.6g      L/H = %10.7g" % ( L, H , L/H)
    return (L,H)

def easytest():
    """
    This test routine demonstrates use of the huffman function, which takes
    a list of simple counts as its input.  It uses the encode function
    to encode a sequence of symbols, [1,2,3,4,3,2,1].  It then uses
    decode to recover the original sequence.
    >>> easytest()
    10010111011101100
    ['1', '2', '3', '4', '3', '2', '1']

    See also the function makenodes for a more sophisticated example.
    See also the file Example.py for a python program that uses this package.
    """
    (c,root) = huffman([1, 2, 3, 4])
    s = encode([1,2,3,4,3,2,1],c)
    print s
    ans = decode( s, root )
    print ans 

def test():
    easytest()
    import doctest
    verbose=1
    if(verbose):
        doctest.testmod(None,None,None,True)
    else:
        doctest.testmod()
    pass

def oldtest(): ## This is the main example. It must be run from a shell and it reads in counts from stdin
## begin read in the list of counts ####################################
    c=[]
    m=0
    print "Reading in frequencies (and optional symbol names) from stdin"
    for line in sys.stdin.readlines():
        if line[0] != '#' :
            words = string.split(line) 
            if len(words) >= 2:
                m += 1 ;  c.append( node( words[0], m, words[1] ) )
            elif len(words) >=1 :
                m += 1 ;  c.append( node( words[0], m ) )
    ## end  read in the list of counts ####################################

    root = iterate ( c )  # make huffman code
    reportcode(c)

def reportcode(c):    
    c.sort(lambda x, y: cmp(x.index, y.index)) # sort by index 
    for co in c :                              # and write the answer
        co.report()    
## end ##########################################################################


    
if __name__ == '__main__':
    import sys
    if sys.argv == [''] : ## probably we have been invoked by C-c C-c in emacs
        test()
        pass
    else : ## read data from stdin and write to stdout
        oldtest()
    pass
