'''
Print Now Playing metadata from TL Icecast server.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import xml.etree.ElementTree as ET
import requests

getxml = requests.get('https://npl.streamguys1.com/admin/stats.xml', auth=('username', 'password'))
getxml = getxml.text

tree = ET.fromstring(getxml)
tree = tree.findall('source')
tree = tree[1] #index of mount with metadata
tree = tree.find('yp_currently_playing').text

print (tree)


