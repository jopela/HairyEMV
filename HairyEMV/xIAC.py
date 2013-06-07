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

    title = "Issuer Action Code (Tag:9F0E,9F0F,9F0D)."

    tmp = [util.unroll(decline), util.unroll(online), util.unroll(default)]
    data = map(list, zip(*tmp))

    colums_header = ["dec", "onl", "def"]

    # Issuer Action Code row headers.
    rows_header_iac = [
            "Offline data authentication not performed",
            "SDA Failed",
            "ICC data missing",
            "Card appears on terminal exception file",
            "DDA failed",
            "CDA failed",
            "RFU",
            "RFU",
            "ICC and terminal diff app versions",
            "Expired application",
            "Application not yet effective",
            "Requested srvice not allowed ",
            "New card",
            "RFU",
            "RFU",
            "RFU",
            "Cardholder verification not successful",
            "Unrecognized CVM",
            "PIN Try Limit exceeded",
            "PIN required, pad not present/working",
            "PIN required, pad present, PIN not entered",
            "Online PIN entered",
            "RFU",
            "RFU",
            "Transaction exceeds floor limit",
            "Lower consecutive offline limit exceed",
            "Upper consecutive offline limit exceeded",
            "Transaction selected rand online processing",
            "Merchant forced transaction online",
            "RFU",
            "RFU",
            "RFU",
            "Default TDOL used",
            "Issuer authentication failed",
            "Script failed before final GENERATE AC",
            "Script failed after final GENERATE AC",
            "RFU",
            "RFU",
            "RFU",
            "RFU"
            ]


    return util.table(title, data, colums_header, rows_header_iac)

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

