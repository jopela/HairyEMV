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

    if args.test:
        doctest.testmod()
        return

    valid_in = validate(afl)

    return

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

    return len(afl) % 8  == 0

if __name__ == "__main__":
    main()

