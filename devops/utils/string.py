def ch(string, offset=0):
    if offset:
        count_ch = len([s for s in string if u'\u4e00' <= s <= u'\u9fa5'])
        if offset > 0:
            return string + (abs(offset) - count_ch - len(string)) * ' '
        else:
            return (abs(offset) - count_ch - len(string)) * ' ' + string
    return string
