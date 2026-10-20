import unicodedata
def align(word):
    count= sum(1 for i in word if unicodedata.east_asian_width(i) in 'WF')
    return count