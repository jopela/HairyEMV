#!/usr/bin/python2

# GLOBAL VARIABLES
PAGE_WIDTH = 80     #page width of a report in char.

import pandas

def unroll(xiac):
    """ Takes an hex string and returns an equivalent binary representation
    of the string, preserving the leading zeros.

    Example
    =======
    >>> unroll("FF")
    '11111111'
    >>> unroll("ABCD")
    '1010101111001101'
    >>> unroll("0a0a0a0a0a")
    '0000101000001010000010100000101000001010'
    """
    size = len(xiac)
    int_val = int(xiac,16)

    nibble_size = 4

    return bin(int_val)[2:].zfill(size*nibble_size)

def rm(string):
    """ Removes arbitraty spaces in strings and .
    
    Example
    =======
    >>> rm('aa    b c d')
    'aabcd'
    >>> rm('00 11 22 33')
    '00112233'
    """
    return "".join([i for i in string if i != ' '])

def is_hex(s):
    """ Returns true if s contains only hexadecimal symbols , that is, only
    0-9 and a,b,c,d,e,f or A,B,C,D,E,F. Returns false otherwise.
    
    Example
    =======
    >>> is_hex('0x000a0a')
    False
    >>> is_hex('00112233445566778899aAbBcCdDeEfF')
    True
    >>> is_hex('001122gg')
    False
    >>> is_hex('')
    False
    >>> is_hex('     ')
    False
    >>> is_hex('  a b c d')
    False
    """

    if len(s) == 0:
        return False

    char_set = set("0123456789abcdefABCDEF")
    s_set = set(s)

    return s_set.issubset(char_set)

def table(title, data, col_header, row_header):
    """ Takes data and returns a string that displays it in a table with the
    added metadata specified by title, col_header and row_header. """

    # Build the table.
    table_text = str(pandas.DataFrame(data,
        index=row_header,
        columns=col_header))

    # Figure out the size of the actual table.
    lines = table_text.splitlines()

    # The size of the table is the largest line from the table itself
    # or the size of the title.
    lengths = [len(i) for i in lines]
    lengths.append(len(title))
    size = max(lengths)

    # Make a proper title.
    title_text = title.center(size) + "\n" + "#" * size + '\n'

    # result is title_text + table_text
    return title_text + table_text 

def die(msg):
    """Print a message on stderr and then exit with error
    status."""
    sys.stderr.write(msg+"\n")
    sys.exit(-1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
