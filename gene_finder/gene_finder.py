#-*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Shane Kelly

"""

from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide

    >>> get_complement('A')
    'T'

    >>> get_complement('C')
    'G'

    Added to check T input
    >>> get_complement('T')
    'A'

    Added to check G input
    >>> get_complement('G')
    'C'
    """
    matchings = {"A": "T", "T" : "A", "G" : "C", "C" : "G"}
    return matchings[nucleotide]

    # if nucleotide == 'A':
    #     return 'T'
    # elif nucleotide == 'T':
    #     return 'A'
    # elif nucleotide == 'C':
    #     return 'G'
    # return 'C'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string

    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'

    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    #Make list, append
    reverseComplement = ''
    for x in xrange(len(dna)):
        reverseComplement = reverseComplement + get_complement(dna[len(dna)-x-1])
    return reverseComplement

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string

    >>> rest_of_ORF("ATGTGAA")
    'ATG'

    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """

#LIST THING 

    restOfOrf = []

    for x in xrange(len(dna)/3):
        #Continue ORF until stop codon
        if dna[3*x:3*x+3] not in ['TAG', 'TAA', 'TGA']:
            restOfOrf.append(dna[3*x:3*x+3])
        else:
            return ''.join(restOfOrf)
    return dna

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Added to check stop codons at the end.
    >>> find_all_ORFs_oneframe("ATCCTAATGCATTAAAAAAAAAAAATGAAAAAATAA")
    ['ATGCAT', 'ATGAAAAAA']

    Added to check multiple short ORFs.
    >>> find_all_ORFs_oneframe("ATGTAGATGTGAATGTAAAAAATGA")
    ['ATG', 'ATG', 'ATG', 'ATGA']
    """

    restOfOrf = ''
    allOrfs = []
    x = 0
    y = 0

    while x <= len(dna)/3:
        # #Look for a start codon
        # for x in range(0, len(dna), 3)
        if dna[3*x:3*x+3] == 'ATG':
            restOfOrf += dna[3*x:3*x+3]
            x += 1
            y = 0
            while x <= len(dna)/3 and y == 0:
                #Continue ORF until a stop codon
                if dna[3*x:3*x+3]  not in ['TAG', 'TAA','TGA']:
                    restOfOrf += dna[3*x:3*x+3]
                    x += 1
                else:
                    allOrfs.append(restOfOrf)
                    restOfOrf = ''
                    x += 1
                    y += 1
            if restOfOrf != '':
                allOrfs.append(restOfOrf)
        else:
            x += 1
    return allOrfs

def find_all_ORFs_oneframe_offset(dna,offset):
    """ Finds all non-nested open reading frames in the variable-given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the variable-given
        frame of the sequence.
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs_oneframe_offset("ATGCATGAATGTAGATAGATGTGCCC", 0)
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Added to check stop codons at the end.
    >>> find_all_ORFs_oneframe_offset("ATCCTAATGCATTAAAAAAAAAAAATGAAAAAATAA", 0)
    ['ATGCAT', 'ATGAAAAAA']

    Added to check multiple short ORFs.
    >>> find_all_ORFs_oneframe_offset("ATGTAGATGTGAATGTAAAAAATGA", 0)
    ['ATG', 'ATG', 'ATG', 'ATGA']

    >>> find_all_ORFs_oneframe_offset("AATGCATGAATGTAGATAGATGTGCCC", 1)
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Added to check stop codons at the end.
    >>> find_all_ORFs_oneframe_offset("AATCCTAATGCATTAAAAAAAAAAAATGAAAAAATAA", 1)
    ['ATGCAT', 'ATGAAAAAA']

    Added to check multiple short ORFs.
    >>> find_all_ORFs_oneframe_offset("AATGTAGATGTGAATGTAAAAAATGA", 1)
    ['ATG', 'ATG', 'ATG', 'ATGA']

    >>> find_all_ORFs_oneframe_offset("AAATGCATGAATGTAGATAGATGTGCCC", 2)
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Added to check stop codons at the end.
    >>> find_all_ORFs_oneframe_offset("AAATCCTAATGCATTAAAAAAAAAAAATGAAAAAATAA", 2)
    ['ATGCAT', 'ATGAAAAAA']

    Added to check multiple short ORFs.
    >>> find_all_ORFs_oneframe_offset("AAATGTAGATGTGAATGTAAAAAATGA", 2)
    ['ATG', 'ATG', 'ATG', 'ATGA']
    """

    restOfOrf = ''
    allOrfs = []
    x = 0
    y = 0

    while x <= len(dna)/3:
        #Look for start codon
        if dna[3*x+offset:3*x+3+offset] == 'ATG':
            restOfOrf += dna[3*x+offset:3*x+3+offset]
            x += 1
            y = 0
            while x <= len(dna)/3 and y == 0:
                codon = dna[3*x+offset:3*x+3+offset]
                #Continue ORF until a stop codon
                if dna[3*x+offset:3*x+3+offset] not in ['TAG', 'TAA','TGA']:
                    restOfOrf += dna[3*x+offset:3*x+3+offset]
                    x += 1
                #Add the ORF to the list of ORFs
                else:
                    allOrfs.append(restOfOrf)
                    restOfOrf = ''
                    x += 1
                    y += 1
            if restOfOrf != '':
                allOrfs.append(restOfOrf)
        else:
            x += 1
    return allOrfs

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """


    return find_all_ORFs_oneframe_offset(dna, 0) + find_all_ORFs_oneframe_offset(dna,1) + find_all_ORFs_oneframe_offset(dna,2)

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string

    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'

    >>> longest_ORF('ACAACGTTTAGTGAAAACG')
    ''
    """
  
    ORFs = find_all_ORFs_both_strands(dna)
    if len(ORFs) > 0:
        longest = ORFs[0]
        for x in xrange(len(ORFs)-1):
            if len(ORFs[x+1]) > len(ORFs[x]):
                longest = ORFs[x+1]
        return longest
    else:
        return ''


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF

    Added to check function. Should most frequently return 19.
    >>> longest_ORF_noncoding("ATGCGAATGTAGCATCAAA", 1000)
    19

    Added to check function. Should most frequently return 90.
    >>> longest_ORF_noncoding("ATCGCACGTCAGCTACGCGCATGCAATGTGCTCGATCGACTAGCCGATCGCGCGATCGCGCGCGGCTAATATATAACCACACTGTGCGAT", 1000)
    90
    """

    currentLength = 0
    for x in xrange(num_trials):
        shuffledORF = longest_ORF(shuffle_string(dna))
        if len(shuffledORF) > currentLength:
             currentLength = len(shuffledORF)
    return currentLength

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

    >>> coding_strand_to_AA("ATGCGA")
    'MR'

    >>> coding_strand_to_AA("ATGCCCGCTTT")
    'MPA'
    """

    aminoAcids = []
    for x in xrange(len(dna)/3):
        codon = dna[3*x:3*x+3]
        aminoAcids.append(aa_table[codon])
    return ''.join(aminoAcids)

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.

    Added to check function.
    >>> gene_finder('ATGCCCGCTTT')
    ['MPA']
    """

    aaSequences = []

    ORFs = find_all_ORFs_both_strands(dna)
    longestNoncodingORF = longest_ORF_noncoding(dna, 1500)
    for element in ORFs:
        #If element is long enough, add it to the list
        if len(element) >= longestNoncodingORF:
            aaSequences.append(coding_strand_to_AA(element))
    return aaSequences

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    dna = load_seq("./data/X73525.fa")
    aaList = gene_finder(dna)
    for element in aaList:
        print element