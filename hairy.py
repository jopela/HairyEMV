#!/usr/bin/python2

CHAR_SET = set("0123456789abcdefABCDEF")
COLORS = ['red','green','white']
NBR_COLORS = len(COLORS)

import argparse
import sys

from termcolor import colored
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
            'decline',
            help='value of the decline xIAC (e.g:FC0011AB00)',
            )

    parser.add_argument(
            'online',
            help='value of the online xIAC (e.g:FC0011AB00)',
            )

    parser.add_argument(
            'default',
            help='value of the decline xIAC (e.g:FC0011AB00)',
            )

    parser.add_argument(
            '-t',
            '--test',
            help='run the doctests',
            default=False,
            action='store_true')

    args = parser.parse_args()

    if args.test:
        print "running doctests. You will see a report for failed tests."
        import doctest
        doctest.testmod()
        print "Done running doctests ... quitting."
        return

    decline = rm(args.decline)
    online = rm(args.online)
    default = rm(args.default)

    valid_in = validate(decline, online, default)

    if not valid_in:
        die("xIAC must all have the same length and be HEX values.")

    print human(decline, online, default)
    return

def human(decline, online, default):
    """ Returns the human readable string for the given xIAC. """

    l = [decline,online,default]
    unrolled = [unroll(xiac) for xiac in l]    

    # The number of bits to display is the lenght of any of the unrolled
    # value.
    nbr_bits = len(unrolled[0])

    lines = [] 

    for i in range(nbr_bits):
        text = "{0}({1},{2},{3})".format(
                (7 - (i % 8)) + 1, # index of the bit in the Byte.
                unrolled[0][i],
                unrolled[1][i],
                unrolled[2][i])

        # A different color is toggled for every bit to display modulo the
        # number of color available.
        ctext = colored(text, COLORS[(i / 8) % NBR_COLORS])

        lines.append(ctext)

    result = "\n".join(lines)
    return result

def rm(string):
    """ Removes arbitraty spaces in strings and .
    
    Example
    =============
    >>> rm('aa    b c d')
    'aabcd'
    >>> rm('00 11 22 33')
    '00112233'
    """
    return "".join([i for i in string if i != ' '])

def unroll(xiac):
    """ Takes an hex string and returns an equivalent binary representation
    of the string.

    Examples
    =============
    >>> unroll("FF")
    '11111111'
    >>> unroll("ABCD")
    '1010101111001101'
    >>> unroll("0a0a0a0a0a")
    '0000101000001010000010100000101000001010'
    """
    size = len(xiac)
    int_val = int(xiac,16)

    nibble_size = 4

    return bin(int_val)[2:].zfill(size*nibble_size)

def validate(decline, online, default):
    """ Returns true if the decline, online and default command line parameters
    are well formated and usable and False if this is not the case.
    
    Examples
    ==============
    >>> validate("0000000000","0000000000","0000000000")
    True
    >>> validate("0000000000","00","0000000000")
    False
    >>> validate("xxxxxxxxxx","0000000000","zzzzzzzzzz")
    False
    >>> validate("0011223344","5566778899","aaBbccDdEE")
    True
    >>> validate("0011223344","5566778899","aaBbffDdEE")
    True
    >>> validate("q011223344","5566778899","aaBbffDdEE")
    False
    """

    # All xIAC must have the same length.
    l = [decline, online, default]
    lengths_ok = len(set([len(i) for i in l])) == 1

    # ALL xIAC must be HEX values.
    l = set(decline+online+default)
    in_char_set = len(l.difference(CHAR_SET)) == 0

    return lengths_ok and in_char_set

def die(msg):
    sys.stderr.write(msg)
    sys.exit(-1)

if __name__ == "__main__":
    main()

