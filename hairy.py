#!/usr/bin/python2

import argparse

def main():

    parser = argparse.ArgumentParser('takes 3 values representing IAC or'\
            ' CIAc and "unroll" them, for human readability')

    parser.add_argument(
            'decline',
            help='value of the decline xIAC (e.g:FC0011AB00)'
            )

    parser.add_argument(
            'online',
            help='value of the online xIAC (e.g:FC0011AB00)'
            )

    parser.add_argument(
            'default',
            help='value of the decline xIAC (e.g:FC0011AB00)'
            )

    args = parser.parse_args()

    print "ARGUMEMTS"
    print "decline:", args.decline
    print "online:", args.online
    print "default:", args.default
    return

if __name__ == "__main__":
    main()

