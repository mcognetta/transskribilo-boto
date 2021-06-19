def get_filter_wordlist():
    f = open('transskribilo/data/filter_wordlist.txt', 'r')
    s = set()
    for line in f:
        line = line.strip()
        s.add(line)
    return s