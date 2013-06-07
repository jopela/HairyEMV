#!/usr/bin/python2

COLORS = ['red','green','white']
NBR_COLORS = len(COLORS)

import argparse
import util
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
        import doctest
        doctest.testmod()
        return

    # xIAC
    decline = util.rm(args.decline)
    online = util.rm(args.online)
    default = util.rm(args.default)

    valid_in = validate(decline, online, default)

    if not valid_in:
        util.die("xIAC must all have the same length and be HEX values.")

    print human(decline, online, default)
    return

def human(decline, online, default):
    """ Returns the human readable string for the given xIAC. """

    l = [decline,online,default]
    unrolled = [util.unroll(xiac) for xiac in l]    

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
    are_hex = util.is_hex(decline+online+default)

    return lengths_ok and are_hex

if __name__ == "__main__":
    main()

