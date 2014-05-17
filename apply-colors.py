#!/usr/bin/env python

from xml.dom import minidom
from sys import stdin, stdout, stderr, argv

if len(argv) < 2:
    print >>stderr, "Usage: apply-colors.py <color-file>"

colors = {}
for line in file(argv[1], "r"):
    fields = line.strip().split(",")
    colors[fields[0]] = fields[1]

dom = minidom.parse(stdin)
for elem in dom.getElementsByTagName('g'):
    id = elem.getAttribute('id')
    if id in colors.keys():
        elem.setAttribute('style', 'fill:#%s' % colors[id])

print dom.toprettyxml()
