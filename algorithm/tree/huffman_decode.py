from heapq import heappush, heappop, heapify
import random, bisect

# Helper routine for generating test sequences
def probchoice(items, probs):
    '''Splits the interval 0.0-1.0 in proportion to probs
    then finds where each random.random() choice lies
    (This routine, probchoice, was released under the
        GNU Free Documentation License 1.2) 13
    '''
    prob_accumulator = 0
    accumulator = []
    for p in probs:
        prob_accumulator += p
        accumulator.append(prob_accumulator)

    while True:
        r = random.random()
        yield items[bisect.bisect(accumulator, r)]

# placeholder
decode = lambda : None

def codecreate(symbol2weights, tutor= False):
    ''' Huffman encode the given dict mapping symbols to weights '''
    global decode
    heap = [ [float(wt), [[sym, []]], repr(sym)] for sym, wt in symbol2weights.iteritems() ]
    heapify(heap)
    if tutor: print "ENCODING:", sorted(symbol2weights.iteritems())
    while len(heap) >1:
        lo = heappop(heap)
        hi = heappop(heap)
        if tutor: print " COMBINING:", lo, '\n AND:', hi
        for i in lo[1]: i[1].insert(0, '0')
        for i in hi[1]: i[1].insert(0, '1')
        lohi = [ lo[0] + hi[0] ] + [lo[1] + hi[1]]
        lohi.append('(%s if nextbit() else %s)' % (hi[2], lo[2]))
        if tutor: print " PRODUCING:", lohi, '\n'
        heappush(heap, lohi)

    wt, codes, decoder = heappop(heap)
    decode = eval('lambda :' + decoder, globals())
    decode.__doc__ = decoder
    for i in codes: i[1] = ''.join(i[1])
    #for i in codes: i[::] = i[:2]
    return sorted(codes, key=lambda x: (len(x[-1]), x))

# Input types
if False:
    tutor = True
    sequencecount = 50
    readin = "B 25 C 2.5 D 12.5 A 5 \n"
    #readin = "a .1 b .15 c .3 d .16 e .29" # Wikipedia sample
    #readin = "a1 .4 a2 .35 a3 .2 a4 .05" # Wikipedia sample
    #readin = "A 50 B 25 C 12.5 D 12.5" # RC example
    cleaned = readin.strip().split()
    symbol2weights = dict((symbol, wt)
                        for symbol, wt in zip(cleaned[0::2], cleaned[1::2]) )

else:
    tutor = True
    sequencecount = 10
    astring = "huffman encoding"
    symbol2weights = dict((ch, astring.count(ch)) for ch in set(astring)) # for astring

huff = codecreate(symbol2weights, tutor= tutor)
print "\nSYMBOL\tWEIGHT\tHUFFMAN CODE"
for h in huff:
    print "%s\t%s\t%s" % (h[0], symbol2weights[h[0]], h[1])

##
## encode-decode check
##
symbol2code = dict(huff)
symbols, weights = zip(*symbol2weights.iteritems())
# normalize weights
weights = [float(wt) for wt in weights]
tot = sum(weights)
weights = [wt/tot for wt in weights]
# Generate a sequence
nxt = probchoice(symbols, weights).next
symbolsequence = [nxt() for i in range(sequencecount)]
# encode it
bitsequence = ''.join(symbol2code[sym] for sym in symbolsequence)

sslen, slen, blen = len(symbolsequence), len(symbols), len(bitsequence)
countlen = len(bin(slen-1)[2:])
print '''

ROUND-TRIPPING
==============
I have generated a random sequence of %i symbols to the given weights.
If I use a binary count to encode each of the %i symbols I would need
%i * %i = %i bits to encode the sequence.
Using the Huffman code, I need only %i bits.
''' % (sslen, slen, sslen, countlen, sslen * countlen, blen )

print "bitsequence", bitsequence
## decoding
nextbit = (bit=='1' for bit in bitsequence).next

decoded = []
try:
    while 1:
        decoded.append(decode())
except StopIteration:
    pass

print "Comparing the decoded sequence with the original I get:", decoded == symbolsequence

