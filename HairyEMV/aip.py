#!/usr/bin/python2

import argparse
import doctest
import pandas
import util


def main():

    parser = argparse.ArgumentParser()

    # parameter for the AIP.
    parser.add_argument(
            'AIP',
            help='Application Interchange Profile (coded in hexadecimal).'
            )

    # doctest flag.
    parser.add_argument(
            '-t',
            '--test',
            help='run the doctests and exit.',
            action='store_true'
            )

    args = parser.parse_args()

    if args.test:
        doctest.testmod()
        return

    valid_in = validate(args.AIP)

    return

def validate(aip):
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

def human(afl):
    """Returns a string that represent the human readable version of the 

if __name__ == "__main__":
    main()

