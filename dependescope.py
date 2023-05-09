#!/usr/bin/env python3

from sys import exit
from sys import argv
from src.client import run


if __name__ == "__main__":
    # file deepcode ignore PT: Validated downstream
    exit(run(argv[1:]))