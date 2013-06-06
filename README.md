Hairy-xIAC
=========

Takes xIAC decline, online and default and print them in a human readable
format.

Introduction
============

xIAC parameters are fixed length byte strings used by credit card payment 
applications. Examples of xIAC settings are IAC (Issuer Action Codes) used
by EMV cards and CIAC (Card Issuer Action Codes) used by MasterCard M/Chip 
product cards. Specification for these card product are often written with 
the same format as the one output by hairy.py, thus making it easy to compare
values of xIAC read from a card with specification values.

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



