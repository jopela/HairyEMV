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
of the 5 bytes value has a particular meaning, it is more common to "unroll"
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

Each column represent the value of the bit for Denial, Online and Default IACs
respectively. Bits in rows are presented from most significant to least 
significant bit. This format allows for easy comparison with documentation
that usually replicate this format for IAC values.

The need for human readable format for EMV parameter arises in many situations.
IAC is an example among many other such as: CDOL, CVM lists, AIP, AFL etc. The
goal of this module is to provide canonical printing for all of these values.


Contact
=======

If you have any questions/comments or, better, if you have a very HIGH paying
job in the banking industry, please contact me at jonathan.pelletier1@gmail.com



