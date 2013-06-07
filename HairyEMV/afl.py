#!/usr/bin/python2

import argparse
import doctest
import util

def main():

    parser = argparse.ArgumentParser()

    # parameter for the AFL.
    parser.add_argument(
            'AFL',
            help='Application File Locator value (coded in hexadecimal).'
            )

    # doctest flag.
    parser.add_argument(
            '-t',
            '--test',
            help='run the doctests and exit.',
            action='store_true'
            )

    args = parser.parse_args()

    test = args.test
    afl = args.AFL

    if test:
        doctest.testmod()
        return

    valid_in = validate(afl)

    if not valid_in:
        util.die("A valid AFL value should be a multiple of 4 Bytes.")

    print human(afl)

    return

def human(afl):
    """ Returns the human readable string for the AFL. """

    l = len(afl) / 8

    texts = []
    for f in range(l):

        sfi = int(afl[0:2],16)
        start_index = int(afl[2:4],16)
        end_index = int(afl[4:6],16)
        signed = int(afl[6:8],16)
        print sfi, start_index, end_index, signed
        text = "({0},{1},{2},{3})".format((sfi & 0xf8) >> 3,
                start_index,
                end_index,
                signed
                )

        texts.append(text)
        afl = afl[8:]


    return "\n".join(texts)

def validate(afl):
    """ Returns True is an AFL is valid on the basis of being a multiple
    of four bytes. 

    Example
    =======

    >>> validate('08010201')
    True
    >>> validate('0801020108010201')
    True
    >>> validate('080102')
    False

    """

    
    return len(afl) % 8  == 0 and len(afl) >= 8

if __name__ == "__main__":
    main()

