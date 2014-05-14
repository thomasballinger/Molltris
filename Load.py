#!/usr/bin/python
#-*- coding: utf-8 -*--

from xml.etree import ElementTree
from RGB import rgbHexDecode
import os.path

DATADIR = "data"
XMLDIR = os.path.join(DATADIR, "XML")
IMAGEDIR = os.path.join(DATADIR, "Images")
MUSICDIR = os.path.join(DATADIR, "Music")

typeConvert = {
        None: lambda x: x,
        "int": int,
        }

def load3NestXml(xml):
    def items(tree):
        for item in tree.getchildren():
            d = {}
            for info in item.getchildren():
                d[info.tag] = typeConvert[dict(info.items()).get("type")](info.text)
            yield d

    return items(ElementTree.XML(xml))

## TODO: Use symbolic values inside the keymap file, instead of numeric literals
def loadHighscores(xml):
    return sorted(load3NestXml(xml), key=lambda x: x["score"])

def _loadKeymaps(xml):
    tree = ElementTree.XML(xml)
    keymaps = {}
    for part in tree.getchildren():
        keymaps[part.tag] = {}
        for mapping in part.getchildren():
            keymaps[part.tag][mapping.tag] = int(mapping.text.strip("\n").strip(" "))
    return keymaps

def loadKeymaps():
    path = os.path.join(XMLDIR, "Keymap.xml")
    print("Loading keymaps from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadKeymaps(rf.read())
    except:
        print("Error while loading keymaps from `{}'".format(path))
        raise ImportError

def _loadTetrominos(xml, verbose=True):
    tree = ElementTree.XML(xml)
    tree_items = dict(tree.items())

    def makeTetromino(text):
        for chars in filter(bool, (l.strip(" ") for l in text.splitlines())):
            line = []
            for char in chars:
                if char == tree_items["true"]:
                    line.append(1)
                elif char == tree_items["false"]:
                    line.append(0)
            yield line

    tetrominos = []
    for sub in tree.getchildren():
        sub_items = dict(sub.items())
        if verbose:
            print("Loading tetromino `{}' with color `{}'".format(sub_items["name"], sub_items["color"]))
        tetrominos.append([
                rgbHexDecode(sub_items["color"]),
                sub_items["name"],
                list(makeTetromino(sub.text)),
                ])

    return tetrominos

def loadTetrominos():
    path = os.path.join(XMLDIR, "Tetrominos.xml")
    print("Loading tetrominos from `{}'".format(path))
    try:
        with open(path) as rf:
            return _loadTetrominos(rf.read())
    except:
        print("Error while loading tetrominos from `{}'".format(path))
        raise ImportError
