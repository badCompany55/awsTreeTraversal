#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AWS CLI

Usage:
    tree_traversal.py -u|--upload <root>...
    tree_traversal.py -bu|--bucketdownload <root> <bucket>
    tree_traversal.py -d|--download...

Options:
    <root> Optional folder name.
"""

from docopt import docopt
from tree_traversal import Graph
import os

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    root = os.getcwd()
    bucket = "zr14cand-devscenario1bucket3833b280-1mvwmcojtfcsq"
    if arguments['<root>']:
        root = arguments['<root>'][0]
    if arguments['<bucket>']:
        bucket = arguments['<bucket>']

    tree = Graph(root, bucket)

    if arguments['--upload']:
        tree.dft()
    if arguments['--download']:
        tree.download_files()

#  tree = Graph("./data/test/ADAJVCLJMUSITWVDAC/BWUIBREVHENTSLFLIT.txt", "zr14cand-devscenario1bucket3833b280-1mvwmcojtfcsq")
#  tree.dft()
#  tree.download_files()





