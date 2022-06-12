#!/usr/bin/env python3
from sys import argv
from os import system
import argparse

from exalang import run

argv = argv[1:]

if len(argv) > 0:
    parser = argparse.ArgumentParser(description="pyexalang -- Python exalang")

    parser.add_argument("file",
                        metavar="FILE",
                        nargs="?",
                        type=argparse.FileType('r'),
                        help="File to run."
                        )

    parser.add_argument("-v",
                        action="count",
                        default=1,
                        help="Verbose output."
                        )

    parser.add_argument("-s",
                        metavar="STRING",
                        type=str,
                        help="Generate a string constant"
                        )

    ns = parser.parse_args()

    # print(ns)

    if(ns.s):
        # Generate a string constant
        # TODO: There's probably better strategies than this
        if(ns.v > 0):
            fmt = "COPY {n:03d} F ; '{c}'"
        else:
            fmt = "COPY {n} F"
        print("GRAB STRING")
        for c in ns.s:
            print(fmt.format(c=c, n=ord(c)))
        exit(0)

    run(ns.file)

    exit()

system(__file__ + " --help")
