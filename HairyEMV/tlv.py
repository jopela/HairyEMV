#!/usr/bin/python2

import argparse
import doctest
import util

def main():

    parser = argparse.ArgumentParser()

    # parameter for the TLV.
    parser.add_argument(
            'TLV',
            help='TLV string (coded in hexadecimal).'
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

    print human(args.TLV)

    return

def head(tlv):
    """ Takes a string containing one or more composite or primitive
    ber-tlv encoded object and returns the first Tag-Lenght-Value triad
    found.
    
    Example
    =======

    >>> head('840E315041592E5359532E4444463031A50E8801015F2D046672656E9F110101') 
    '840E315041592E5359532E4444463031'
    >>> head('840')
    ''
    
    """
    return "please implement me !"

def tail(tlv):
    """ Takes a string containing one or more composite or primitive ber-tlv
    encoded object and returns everything but the first Tag-Length-Value triad
    found.
    
    Example
    =======

    >>> tail('840E315041592E5359532E4444463031A50E8801015F2D046672656E9F110101')
    'A50E8801015F2D046672656E9F110101'
    
    """
    return "please implement me!"

def find(tag, tlv):
    """ Takes tlv and search for tag, returning the Tag-Length-Value triad
    associated with it if found. 
    
    Example
    =======
    >>> find('9F11','6F20840E315041592E5359532E4444463031A50E8801015F2D046672656E9F110101')
    '9F110101'
    """

    return "please implement me!"

def children(tlv):
    """ Takes a ber-tlv encoded object and return the list of tlv data object
    contained in it's value field.

    Example
    =======

    >>> children('6f20840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101')
    '840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101'

    """

    return "please implement me"

def primitive(tlv):
    """ Takes a ber-tlv encoded object and returns True if it is a primitive
    object. Returns false if it is constructed. 
    
    Example
    =======

    >>> primitive('6f20840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101')
    False
    >>> primitive('9f110101')
    True
    """

    b = int(tlv[0],16)
    
    return (b & 2) == 0

def tag(tlv):
    """ Returns the first tag value found in the ber-tlv encoded object. 
    
    Example
    =======

    >>> tag('9f110101')
    '9f11'
    >>> tag('840e315041592e5359532e4444463031')
    '84'
    >>> tag('a50e8801015f2d046672656e9f110101')
    'a5'
    """

    return 'a5'

def length(tlv):
    """ Returns the first lenght field found in the ber-tlv encoded object.
    
    Example
    =======

    >>> tag('9f110101')
    '01'
    >>> tag('840e315041592e5359532e4444463031')
    '0e'
    >>> tag('a50e8801015f2d046672656e9f110101')
    '0e'
    
    """
    return '0e'

def value(tlv):
    """ Return the value field of a ber-tlv encoded object.

    Example
    =======

    >>> value('9f110101')
    '01'
    >>> value('840e315041592e5359532e4444463031')
    '315041592e5359532e4444463031'

    """
    return '01'

def human(tlv,depth=0,indent=2):
    """ Returns the human readable string for the TLV input.
    
    Example
    =======

    >>> human('6f20840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101')
    6F - [32]
      82 - [14] - 315041592E5359532E4444463031
      A5 - [14]
        88 - [1] - 01
        5F2D - [4] - 6672656E
        9F11 - [1] - 01
    """
    # String format used to print.
    basic_format = "{0}{1} - [{2}]"
    primitive_format = basic_format + " - {3}"
    # shortcut for getting the right indentation depending on the depth.
    f = lambda x : ' ' * indent * x
    
    # These are printed in the base case as well as in the recursive case.
    t = tag(tlv)
    l = length(tlv)

    # Base case.
    if primitive(tlv):
        v = value(tlv)
        return primitive_format.format(f(depth),t,l,v)

    # Recursive definition.
    lines = [basic_format.format(f(depth), t, l)]
    new_depth = depth + 1
    for c in children(tlv):
        lines.append(human(c,new_depth))

    return "\n".join(lines)

if __name__ == "__main__":
    main()

