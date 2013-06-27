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

def bitlist(size):
    """ Returns a bit list to be displayed as a Bit column in the data table.
    
    Example
    =======

    >>> bitlist(2)
    [8, 7, 6, 5, 4, 3, 2, 1, 8, 7, 6, 5, 4, 3, 2, 1]
    
    """

    bit_per_byte = 8
    atom = range(8,0,-1)

    return atom * size

def bytelist(size):
    """ Returns a Byte list to be displayed as a Byte column in the data table.

    Example
    =======

    >>> bytelist(2)
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    """

    space = " "
    bit_per_byte = 8
    result = []
    for i in range(size*bit_per_byte):
        if i % bit_per_byte == 0:
            placeholder = str(i/bit_per_byte + 1)
            result.append(placeholder)
        else:
            result.append(space)
        
    return result

def human(decline, online, default):
    """ Returns the human readable string for the given xIAC. """

    decline_col = util.unroll(decline)
    online_col = util.unroll(online)
    default_col = util.unroll(default)

    tmp = [decline_col, online_col, default_col]
    data = map(list, zip(*tmp))

    size = len(tmp[0])

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

    # Card Issuer Action Code row headers (MasterCard specific).
    rows_header_ciac = [
            "RFU",
            "Unable to go online",
            "Offline PIN verif Not Performed",
            "Offline PIN Verification Failed",
            "PIN Try Limit exceeded",
            "International Transaction",
            "Domestic Transaction",
            "Terminal Wrongly Considers Off PIN OK",
            "Lower Consecutive Offiline Limit Exceeded",
            "Upper Consecutive Offiline Limit Exceeded",
            "Lower Cumulative Offiline Limit Exceeded",
            "Upper Cumulative Offiline Limit Exceeded",
            "Go Online On Next Transaction Was Set",
            "Issuer Authentication Failed",
            "Script Received",
            "Script Failed",
            "RFU",
            "RFU",
            "RFU",
            "RFU",
            "RFU",
            "RFU",
            "Match Found in Additional Check Table",
            "No Match Found In Additional Check Table"]


    # Select the right title and rows_header list.
    if len(rows_header_iac) == size:
        title = "Issuer Action Code (Tag:9F0E,9F0F,9F0D)."
        rows = rows_header_iac
    elif len(rows_header_ciac) == size:
        title = "CARD Issuer Action Code (Tag:C3/CF,C5/CE,C4/CD)."
        rows = rows_header_ciac
        title
    else:
        rows = range(1,size+1)


    return util.table(title, data, colums_header, rows)

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

