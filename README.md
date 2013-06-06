HairyEMV
=========

A python package for the human readability of financial card parameter.  

Introduction
============

HairyEMV is a package containing scripts that help print, in a human readable
format, some of the data that can be read from an EMV compliant application
card. One example of such paramters are IAC (Issuer Action Codes), which is a 
set of 3 EMV tags that tell a transaction terminal what is the behavior of the
card involved in the current transaction. IACs values are read from a 
card and usually presented as hexadecimal-coded integer. Typical values for
IACs tag set (Denial, Online, Default) could be 0000000000, BC70BC9800 and 
BC50BC8800. This is a valid representation for IAC values but since each bit
of the 5 bytes value as a particular meaning, it is more common to "unroll"
them and to print to corresponding bit of each IAC tag next to each other. For
the values of the IAC tags shown above, the "canonical" representtion would be:

    8(0,1,1)
    7(0,0,0)
    6(0,1,1)
    5(0,1,1)
    4(0,1,1)
    3(0,1,1)
    2(0,0,0)
    1(0,0,0)
    8(0,0,0)
    7(0,1,1)
    6(0,1,0)
    5(0,1,1)
    4(0,0,0)
    3(0,0,0)
    2(0,0,0)
    1(0,0,0)
    8(0,1,1)
    7(0,0,0)
    6(0,1,1)
    5(0,1,1)
    4(0,1,1)
    3(0,1,1)
    2(0,0,0)
    1(0,0,0)
    8(0,1,1)
    7(0,0,0)
    6(0,0,0)
    5(0,1,0)
    4(0,1,1)
    3(0,0,0)
    2(0,0,0)
    1(0,0,0)
    8(0,0,0)
    7(0,0,0)
    6(0,0,0)
    5(0,0,0)
    4(0,0,0)
    3(0,0,0)
    2(0,0,0)
    1(0,0,0)

each column represent the value of the bit for Denial, Online and Default IACs
respectively. Bits in row are presented from most significant to least 
significant bit.

Requirements
============

The only external dependency is termcolor. If you have pip installed on your 
system, just issue the following command:

    pip install termcolor

Usage
=====

example usage:

    hairy.py bf0c00112433 ba0c00112233 de0c00512233  

if you provide your xIAC in quotes, hairy.py will manage any spaces in the
xIACs values making this:

    hairy.py "bf 0c 00 11 24 33" ba0c00112233 de0c00512233  

A valid invocation.

TODO
====

1. Add support for xIAC comparison.

Contact
=======

If you have any questions/comments or, better, if you have a very HIGH paying
job in the banking industry, please contact me at jonathan.pelletier1@gmail.com



