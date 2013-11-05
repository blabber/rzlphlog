# -*- coding: iso-8859-15 -*-

import urllib
import string
import argparse
import os.path
import json

STATUSURI = 'https://status.raumzeitlabor.de/api/full.json'

GOPHERMAPTEMPLATE = string.Template(
"""      ___                 ____    _ _   ___ _        _
     | _ \__ _ _  _ _ __ |_  /___(_) |_/ __| |_ __ _| |_ _  _ ___
     |   / _` | || | '  \ / // -_) |  _\__ \  _/ _` |  _| || (_-<
     |_|_\__,_|\_,_|_|_|_/___\___|_|\__|___/\__\__,_|\__|\_,_/__/
                                             Hackerspace Mannheim
                              Digitalkultur im Rhein-Neckar-Kreis

=================================================================
hDer RaumZeitStatus im WWW	GET /	status.raumzeitlabor.de	80
=================================================================

Das RaumZeitLabor ist $tuer und $geraete Geraete sind aktiv.

Identifizierte kohlenstoffbasierte Lebensformen:

$laboranten

=================================================================
""")

def normalize(string):
	string = string.replace(u"�", "Ae").replace(u"�", "ae")
	string = string.replace(u"�", "Oe").replace(u"�", "oe")
	string = string.replace(u"�", "Ue").replace(u"�", "ue")
	string = string.replace(u"�", "ss")
	string = string.encode("ascii", "ignore")
	return string

def create_gophermap(dirname, json):
	d = { 'tuer' : 'offen' if json['details']['tuer'] else 'geschlossen',
		'geraete' : json['details']['geraete'],
		'laboranten' : '\n'.join('    {0}'.format(n)
				for n
				in json['details']['laboranten'])
			if len(json['details']['laboranten'])
			else '    (niemand)'
		}
	gophermap = os.path.join(dirname, 'gophermap');
	with open(gophermap, 'w') as file:
		file.write(GOPHERMAPTEMPLATE.substitute(d))

def get_json(uri):
	u = urllib.urlopen(uri)
	j = u.read()
	u.close()
	return json.loads(j)

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(
		description='Create a phlog from the RaumZeitLabor feed.')
	argparser.add_argument('--dir', '-d', dest='dir', default=os.getcwd(),
		action='store', help='The target directory')
	args = argparser.parse_args()
	target = os.path.realpath(args.dir)
	create_gophermap(target, get_json(STATUSURI))
