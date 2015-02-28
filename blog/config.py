import json

try:
    f = open('config.json', 'r')
except IOError, e:
    print 'Configure your config.json'
    print 'I/O Error', e.strerror
    exit(-1)
else:
    info = json.load(f)