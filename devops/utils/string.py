def cn_format(string, offset=0):
    if offset:
        count_ch = len([s for s in string if cn_check(s)])
        if offset > 0:
            return string + (abs(offset) - count_ch - len(string)) * ' '
        else:
            return (abs(offset) - count_ch - len(string)) * ' ' + string
    return string

def cn_check(s):
    return u'\u4e00' <= s <= u'\u9fa5'
