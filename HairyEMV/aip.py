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

    if not valid_in:
        util.die("a valid AIP has a lenght of 2 Bytes and is code in HEX")

    print human(args.AIP)

    return

def validate(aip):
    """ Returns True is AIP is valid on the basis of having a lenght of
    2 bytes hex coded values. 

    Example
    =======

    >>> validate('3900')
    True
    >>> validate('1980')
    True
    >>> validate('198g')
    False
    >>> validate('090')
    False
    >>> validate('00090')
    False

    """

    return len(aip) == 4 and util.is_hex(aip)

def human(aip):
    """Returns a string that represent the human readable version of the ."""

    title = "Application Interchange Profile (tag: 0x82)"
    data =[[i] for i in util.unroll(aip)]
    col_header = ["Value"]
    row_header = [
            "RFU",
            "SDA supported",
            "DDA supported",
            "Cardholder verification is supported",
            "Terminal risk management is to be performed",
            "Issuer authentication is supported",
            "RFU",
            "CDA supported",
            "Reserved for us by the EMV Contactless Specifications"
            ] + ["RFU"] * 7

    return util.table(title, data, col_header, row_header)

if __name__ == "__main__":
    main()

