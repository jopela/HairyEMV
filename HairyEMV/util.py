#!/usr/bin/python2

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

def die(msg):
    """Print a message on stderr and then exit with error
    status."""
    sys.stderr.write(msg+"\n")
    sys.exit(-1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
