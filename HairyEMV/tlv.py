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
    
    if not validate(args.TLV):
        util.die("A valid TLV value must be encoded in HEX and be an integer"\
                "multiple of Bytes greater then 0")


    print human(args.TLV)

    return

def validate(tlv):
    """ Validate a ber-tlv encoded string on the basis that it's made up only
    of HEX symbol and that it is made up of bytes (even length).

    Example
    =======
    >>> validate('9f110101')
    True
    >>> validate('840E315041592E5359532E4444463031')
    True
    >>> validate('')
    False
    >>> validate('0x9f110101')
    False

    """

    return (len(tlv) % 2 == 0) and util.is_hex(tlv)

# TODO: what should head return when tlv values are incorrect?
def head(tlv):
    """ Takes a string containing one or more composite or primitive
    ber-tlv encoded object and returns the first Tag-Lenght-Value triad
    found.
    
    Example
    =======

    >>> head('840E315041592E5359532E4444463031A50E8801015F2D046672656E9F110101') 
    '840E315041592E5359532E4444463031'
    
    """
    t = tag(tlv)
    l = length(tlv)
    v = value(tlv)

    return t+l+v

def tail(tlv):
    """ Takes a string containing one or more composite or primitive ber-tlv
    encoded object and returns everything but the first Tag-Length-Value triad
    found.
    
    Example
    =======

    >>> tail('840E315041592E5359532E4444463031A50E8801015F2D046672656E9F110101')
    'A50E8801015F2D046672656E9F110101'
    
    """

    # tail is list minus the slice of head.
    h = head(tlv)

    return tlv[len(h):]

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
    ['840e315041592e5359532e4444463031', 'a50e8801015f2d046672656e9f110101']
    >>> children('a50e8801015f2d046672656e9f110101')
    ['880101', '5f2d046672656e', '9f110101']
    >>> children('9f110101')
    []

    """

    childs = []
    if primitive(tlv):
        return childs

    v = value(tlv)

    while v:
        childs.append(head(v))
        v = tail(v)

    return childs

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

    # A tag always include at least 1 byte.
    t = tlv[0:2]

    bin_t = int(t, 16)
    sub_mask_1 = 0x1F
    sub_mask_2 = 0x80

    # More bytes follow if & result with sub_mask_1 == sub_mask_1
    if (bin_t & sub_mask_1) == sub_mask_1:
        while True:
            temp = tlv[len(t):len(t)+2]
            t += temp
            bin_temp = int(temp, 16)
            # Even more by follow if the current msb of the Byte is 1
            if (bin_temp & sub_mask_2 == 0):
                return t
    else:
        return t

# TODO: add test for case of more than 1 bytes for length tag.
def length(tlv):
    """ Returns the first lenght field found in the ber-tlv encoded object.
    
    Example
    =======

    >>> length('9f110101')
    '01'
    >>> length('840e315041592e5359532e4444463031')
    '0e'
    >>> length('a50e8801015f2d046672656e9f110101')
    '0e'
    
    """
    
    # get rid of the tag first.
    l = len(tag(tlv))

    notag = tlv[l:]

    b_bit = int(notag[0:2],16)
    sub_mask = 0x80
    nbr_bytes = 0

    if b_bit & sub_mask:
        nbr_bytes = 0x7F & b_bit
    else:
        nbr_bytes = 1

    return notag[0:nbr_bytes*2]

# TODO: this function is HARD to read ... add comments or refactor into
# cleaner code.
def value(tlv):
    """ Return the value field of a ber-tlv encoded object. If the string 
    contains 2 primitive object, returns the value of the first one.

    Example
    =======

    >>> value('9f110101')
    '01'
    >>> value('840e315041592e5359532e4444463031')
    '315041592e5359532e4444463031'
    >>> value('840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101')
    '315041592e5359532e4444463031'

    """

    # Retrieve the tag field of the object.
    tag_field = tag(tlv)

    # Retrieve the length field from the object.
    len_field = length(tlv)

    # Compute the real length.
    l_bit = int(len_field[0:2],16) 
    real_len = 0
    if l_bit & 0x80:
        real_len = int(len_field[2: 2 + (l_bit & 0x7F) * 2]) 
    else:
        real_len = l_bit * 2

    # combined length of tag + length fields
    combined = len(tag_field+len_field)
    
    return tlv[combined:combined+real_len] 

def human(tlv,depth=0,indent=2):
    """ Returns the human readable string for the TLV input.
    
    Example
    =======

    #TODO: find a way to test this? 
    #>>> human('6f20840e315041592e5359532e4444463031a50e8801015f2d046672656e9f110101')
    #'6f - [32]\n  84 - [14] - 315041592e5359532e4444463031\n  a5 - [14]\n    88 - [1] - 01\n    5f2d - [4] - 6672656e\n    9f11 - [1] - 01'
    
    """
    # String format used to print.
    basic_format = "{0}{1} - [{2}]"
    primitive_format = basic_format + " - {3}"
    # shortcut for getting the right indentation depending on the depth.
    f = lambda x : ' ' * indent * x
    
    # These are printed in the base case as well as in the recursive case.
    t = tag(tlv)
    l = int(length(tlv),16)

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

