#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 STX Next Sp. z o.o. and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
@author: Igor Kupczyński <igor.kupczynski[at]stxnext.pl>
"""

import colorsys
import csv
import sys

from PIL import Image


def _to_hsv(r, g, b):
	h, s, v = colorsys.rgb_to_hsv(float(r)/256, float(g)/256, float(b)/256)
	return (int(h * 360), s, v)

def _to_rgb(h, s, v):
	r, g, b = colorsys.hsv_to_rgb(float(h)/360.0, s, v)
	return (int(r*256), int(g*256), int(b*256))

def _apply_transform(table, r, g, b):
	h, s, v = _to_hsv(r, g, b)
	return _to_rgb(table[h], s, v)

class Converter(object):
	"""
	Converts colors in an image.
	
	Usage:
	
	To convert orange (32/360 in HSV) to green (98/360) and blue (209/360)
	to violet (295/360). The threshold is set to 10/360 in both cases.
	SV from HSV are preserved. 
	
	>>> conversions = [(32, 98, 10), (209, 295, 10)]
	>>> c = Converter.create(conversions)
	
	>>> from PIL import Image
	>>> im = Image.open('in.jpg')
	
	>>> new_im = c.do_conversion(im)
	>>> new_im.save('out.jpg', quality=95, optimize=True)
	"""
	
	def __init__(self, table):
		self.table = table
	
	@classmethod
	def create(klass, conversions):
		table = {}
		for h in xrange(0, 360):
			table[h] = h
			for (fr, to, th) in conversions:
				base = fr
				delta = to - fr
				if (h <= klass._move(base, th)) and (h >= klass._move(base, -th)):
					table[h] = klass._move(h, delta)
					break
		return klass(table)
	
	@classmethod
	def _move(klass, h, delta):
		r = h + delta
		if r > 1.0:
			return r - 1.0
		if r < 0.0:
			return r + 1.0
		else:
			return r
	
	def do_conversion(self, im):
		res = im.copy()
		res.putdata([_apply_transform(self.table, r, g, b) for (r, g, b) in \
					 res.getdata()])
		return res

def main(args):
	if len(args) != 4:
		print "USAGE: %s <rules-file> <in-file> <out-file>" % sys.argv[0]
		sys.exit(-1)
	conversions = []
	with open(args[1], 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if (len(row) == 3):
				conversions.append((int(row[0]), int(row[1]), int(row[2])))
	if not conversions:
		print "ERROR: rules file empty"
		sys.exit(-1)
	c = Converter.create(conversions)
	im = Image.open(args[2])
	result = c.do_conversion(im)
	result.save(args[3], quality=100)
	
	
if __name__ == '__main__':
	main(sys.argv)		