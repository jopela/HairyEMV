#!/usr/bin/python2

import argparse
import doctest
import util


def main():

    parser = argparse.ArgumentParser()

    # parameter for the CVM list.
    parser.add_argument(
            'CVM',
            help='Cardholder Verification Method list (coded in hexadecimal).'
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

    valid_in = validate(args.CVM)

    if not valid_in:
        util.die("CVM list must contain 8 bytes for amount x and y and at least"\
                " 2 bytes for one CVM")

    print human(args.CVM)
    return

def validate(cvm):
    """ Returns True if the CVM list is valid on the basis of having the
    right amount of bytes for amounts x and y + bytes for a t least 1 cmv
    list. Each subsequent CVM must be 2 bytes long. CVM

    Example
    =======

    >>> validate('00000000000000004103')
    True
    >>> validate('000000000000010141035e03')
    True
    >>> validate('0000004103')
    False
    >>> validate('00004103')
    False
    >>> validate('00000000004103')
    False
    >>> validate('')
    False

    """

    return len(cvm) >= 12 and (len(cvm) - 12) % 4 == 0 and util.is_hex(cvm)

def human(cvm):
    """Returns a string that represent the human readable version of the
    CVM list."""

    title = "Cardholder Verification Method list (tag:0x8E)"
    
    # for a valid CVM list, the first 8 bytes are reserved for the amounts.
    amounts = cvm[:16]

    # card verification methods.
    cvms = cvm[16:]

    # each CVM is 4 nibbles long.
    nbr_cvms = len(cvms) / 4

    # order of appearance in the CVM list.
    orders = range(1,nbr_cvms+1)

    # cvm values.
    values = [cvms[i:i+4] for i in range(0, len(cvms), 4)]

    # list of cvm methods.
    method_list = [method(i) for i in values]

    # list of failure behavior.
    failure_list = [fail(i) for i in values]

    # conditions.
    condition_list = [condition(i) for i in values]

    tmp = [values, method_list, failure_list, condition_list]

    data = map(list, zip(*tmp))

    col_header = ["Value","Method","Fail", "condition"]
    row_header= orders

    return util.table(title, data, col_header, row_header) +"\n" +\
    "Amount X:{0}\nAmount Y:{1}".format(int(amounts[:4],16),int(amounts[4:],16)) 

def method(cvm):
    """ Takes a cvm and return a string description of the method associated
    with it.

    Example
    =======
    >>> method('0000')
    'Fail CVM'
    >>> method('4103')
    'Plaintext PIN'
    >>> method('4201')
    'Online PIN'
    >>> method('0303')
    'Plaintext PIN and signature'
    >>> method('4403')
    'Enciphered PIN'
    >>> method('4501')
    'Enciphered PIN and signature'
    >>> method('1E03')
    'Signature'
    >>> method('1F01')
    'No CVM'
    >>> method('3F00')
    'Unavailable'
    >>> method('4700')
    'RFU'
    >>> method('2F02')
    'Reserved by payment system'
    >>> method('3100')
    'Reserved by issuer'
    """

    method_db = {
            0x00:"Fail CVM",
            0x01:"Plaintext PIN",
            0x02:"Online PIN",
            0x03:"Plaintext PIN and signature",
            0x04:"Enciphered PIN",
            0x05:"Enciphered PIN and signature",
            0x1E:"Signature",
            0x1F:"No CVM",
            0x3F:"Unavailable"
            }

    mask = 0x3F

    m = int(cvm[:2],16) & mask

    # test for the possible cases of CVM.
    if m in method_db:
    # This is one of the "regular" CVM, return it.
        return method_db[m]
    elif m >= 0x06 and m <= 0x1D:
    # Range reserved for future use by EMV.
        return "RFU"
    elif m >= 0x20 and m <= 0x2F:
    # Range reserved by individual payment system.
        return "Reserved by payment system"
    elif m >= 0x30 and m <= 0x3E:
    # Range reserved by issuers
        return "Reserved by issuer"
    else:
        return "Unknown"

def fail(cvm):
    """ Returns True is we must fail CVM after this method has failed. False
    if not. 
    
    Example
    =======
    >>> fail('4203')
    False
    >>> fail('0201')
    True
    """

    mask = 0x4
    f = int(cvm[0],16) & mask

    return f == 0

def condition(cvm):
    """ Takes a cvm and return a string description of the method associated
    with it.

    Example
    =======

    >>> condition('4200')
    'Always'
    >>> condition('4201')
    'Unattended cash'
    >>> condition('4202')
    '!unattend cash & !manual cash & !purchase + cashback'
    >>> condition('4203')
    'Terminal supports the CVM'
    >>> condition('4204')
    'Manual cash'
    >>> condition('4205')
    'Purchase with cashback'
    >>> condition('4206')
    'In app cur and under x'
    >>> condition('4207')
    'In app cur and over x'
    >>> condition('4208')
    'In app cur and under y'
    >>> condition('4209')
    'In app cur and over y'
    >>> condition('420B')
    'RFU'
    >>> condition('42FF')
    'Reserved by individual payment systems'

    """

    condition_db = {
            0x00:"Always",
            0x01:"Unattended cash",
            0x02:"!unattend cash & !manual cash & !purchase + cashback",
            0x03:"Terminal supports the CVM",
            0x04:"Manual cash",
            0x05:"Purchase with cashback",
            0x06:"In app cur and under x",
            0x07:"In app cur and over x",
            0x08:"In app cur and under y",
            0x09:"In app cur and over y"
            }

    c = int(cvm[2:],16)

    if c in condition_db:
    # if the condition is in the database, return the corresponding string.
        return condition_db[c]
    elif c >= 0x0A and c <= 0x7F:
    # Reserved for future use.
        return 'RFU'
    else:
    # Reserved by payment systems.
        return 'Reserved by individual payment systems'

if __name__ == "__main__":
    main()

