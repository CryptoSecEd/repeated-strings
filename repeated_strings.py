#!/usr/bin/env python3

"""This script will search for repeated strings in a text file
(above a minimum length).
"""

import re
import sys
from argparse import ArgumentParser
import docx


def longest(text, i, j, min_len):
    """ Find the longest length for which the substrings at two offsets
    are the same.

    :param text: The string in question
    :type text: ``str``
    :param i: The first offset
    :type i: ``int``
    :param j: The second offset
    :type j: ``int``
    :param min_len: The known length that the offset strings match
    :type min_len: ``int``
    :raises ValueError: If the offsets do not match for the first "min"
    characters
    :rtype: ``int``
    """
    length = min_len
    first = text[i:i+length]
    second = text[j:j+length]
    if first != second:
        raise ValueError("Initial string mismatch in longest(): %s %s"
                         % (first, second))
    same = True
    while same:
        length = length+1
        first = text[i:i+length]
        second = text[j:j+length]
        if first != second:
            same = False
    length = length-1
    position1 = int(100*i/len(text))
    position2 = int(100*j/len(text))
    print("Match of length: %d at offsets %d %d (%d%% and %d%%)"
          % (length, i, j, position1, position2))
    print(first[:-1])
    return length


def main():
    """Read the contents of the file, extract the characters and use
    the longest() function to find the repeated strings.
    """
    parser = ArgumentParser(
        description="Find repeated strings in a text file")
    parser.add_argument("--source", help="Source file to examine")
    parser.add_argument("--minlen",
                        help="Minimum length of match to search for",
                        default=50)
    parser.add_argument("--docx", help="Parse a .docx source file",
                        action="store_true")

    args = parser.parse_args()

    if not args.source:
        print("Please specify the source file.")
        sys.exit(1)

    parts = {}

    # Obtain all text from the source document, whether it is a .docx or
    # a text file
    if args.docx:
        letters_only = ""
        try:
            doc = docx.Document(args.source)
        except IOError:
            print("Could not open file '%s'" % args.source)
            sys.exit(1)
        all_paras = doc.paragraphs
        for para in all_paras:
            letters_only = (letters_only
                            + "".join(re.findall("[a-zA-Z]+", str(para.text))))
    else:
        try:
            file_in = open(args.source, 'r')
        except IOError:
            print("Could not open file '%s'" % args.source)
            sys.exit(1)
        all_text = file_in.read()
        letters_only = "".join(re.findall("[a-zA-Z]+", all_text))

    length = 0

    args.minlen = int(args.minlen)

    # Loop through the text file using a sliding window of length
    # args.minlen. The parts dictionary starts empty. If the window is
    # not in parts, then it is added and the window shifts by one. If it
    # is, then use the longest() function to determine how long the
    # match is.
    for i in range(0, len(letters_only)-args.minlen):
        if length != 0:
            i = i + 1
            length = length - 1
        else:
            current = letters_only[i:i+args.minlen]
            if current in parts:
                length = longest(letters_only, parts[current], i, args.minlen)
            else:
                parts[current] = i


if __name__ == "__main__":
    main()
