
def rgbHexDecode(s):
    """
    >>> rgbHexDecode("#FFFFFF")
    (255, 255, 255)
    >>> rgbHexDecode("FFFFFF")
    (255, 255, 255)
    """
    if s[0] == "#":
        s = s[1:]
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
