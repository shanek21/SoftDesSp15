class DNASequence(object):
    """ Represents a sequence of DNA """
    def __init__(self, nucleotides):
        """ constructs a DNASequence with the specified nucleotides.
             nucleotides: the nucleotides represented as a string of
                          capital letters consisting of A's, C's, G's, and T's """
        self.nucleotides = nucleotides

    def __str__(self):
        """ Returns a string containing the nucleotides in the DNASequence
        >>> seq = DNASequence("TTTGCC")
        >>> print seq
        TTTGCC
        """
        return self.nucleotides

    def get_reverse_complement(self):
        """ Returns the reverse complement DNA sequence represented
            as an object of type DNASequence

            >>> seq = DNASequence("ATGC")
            >>> rev = seq.get_reverse_complement()
            >>> print rev
            GCAT
            >>> print type(rev)
            <class '__main__.DNASequence'>
        """
        matchings = {"A": "T", "T" : "A", "G" : "C", "C" : "G"}
        dna = self.nucleotides
        reverseComplement = ''
        for x in xrange(len(dna)):
            reverseComplement = reverseComplement + matchings(dna[len(dna)-x-1])

        return reverseComplement

    def get_proportion_ACGT(self):
        """ Computes the proportion of nucleotides in the DNA sequence
            that are 'A', 'C', 'G', and 'T'
            returns: a dictionary where each key is a nucleotide and the
                corresponding value is the proportion of nucleotides in the
            DNA sequence that are that nucleotide.
            (NOTE: this doctest will not necessarily always pass due to key
                    re-ordering don't worry about matching the order)
        >>> seq = DNASequence("AAGAGCGCTA")
        >>> d = seq.get_proportion_ACGT()
        >>> print (d['A'], d['C'], d['G'], d['T'])
        (0.4, 0.2, 0.3, 0.1)
        """
        nucleo = list(self.nucleotides)
        d = dict()
        for N in nucleo:
            if N not in d:
                d[N] = 1
            else:
                d[N] += 1
        total = d['A'] + d['T'] + d['C'] + d['G']
        prop = dict()
        prop['A'] = d['A']/float(total)
        prop['C'] = d['C']/float(total)
        prop['G'] = d['G']/float(total)
        prop['T'] = d['T']/float(total)

        return prop

if __name__ == '__main__':
    import doctest
    doctest.testmod()
