#!/usr/bin/env python3
# svg_parser.py
# A python program to generate points from and svg file
import bs4 as bs
from sys import argv

def get_d(filename):
# Replace argv with filename etc
    source = open(argv[1], 'r')

    soup = bs.BeautifulSoup(source, 'xml')

    # This doesnt have support for multiple d or paths
    path = soup.find('path')

    ctrl_points = path.get('d')

    return ctrl_points


def main(filename):
    pass

if __name__ == "__main__":
    main(argv[0])
