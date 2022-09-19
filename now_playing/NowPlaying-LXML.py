'''
Print Now Playing metadata from TL Icecast server.

please note: lxml is not in core Python. Install via PIP.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from lxml import html

source = ('http://npl.streamguys1.com/status.xsl')
root = html.parse(source)
element = root.xpath('//td/text()')[18]
print (element)

#https://stackoverflow.com/questions/4771754/how-to-use-lxml-to-find-element-text-in-xhtml-document
