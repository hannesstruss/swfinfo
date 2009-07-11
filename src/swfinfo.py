#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of SWFInfo.
# 
# Copyright 2009 Hannes Struß <x@hannesstruss.de>
# 
# SWFInfo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# SWFInfo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SWFInfo.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import with_statement

import sys
import math
import zlib

RESULT_FIELDS = (
	"Version",
	"Compressed",
	"Uncompressed Size",
	"Compressed Size",
	"Stage Dimensions",
)

def analyze(path):
	result = {}
	with open(path, "rb") as file_obj:
		buffer = file_obj.read(8)
		
		compressed = buffer[0] == "C"
		
		compressed_content = file_obj.read()
		uncompressed_content = zlib.decompress(compressed_content)

		result["Compressed"] = "yes" if compressed else "no"
		result["Version"] = ord(buffer[3])
		result["Uncompressed Size"] = parse_int(buffer[4:8])
		result["Compressed Size"] = len(compressed_content) + 8
		result["Stage Dimensions"] = map(lambda x: x/20.0, parse_rect(uncompressed_content, 0)[1::2])
		
		return result

def parse_rect(bytes, index):
	"""
	parses a RECT structure.
	@param bytes: the bytes to parse the RECT from
	@param index: the index of the nbits of the RECT
	@return: a tuple, (width, height) 
	"""
	result = []

	nbits = ord(bytes[index]) >> 3
	rect_len = int(math.ceil((nbits * 4 + 5) / 8.0)) # number of bytes the rect needs, including nbits
	
	offset = 5
	for n in xrange(4): # read 4 bitvalues
		first_byte = offset / 8 + index
		bitval_length = int(math.ceil(((offset % 8) + nbits) / 8.0))
		result.append(parse_SB(
			bytes[first_byte:][:bitval_length], 
			nbits, 
			offset % 8))
		
		offset += nbits
	
	return tuple(result)
	
def parse_SB(bytes, nbits, offset):
	"""
	parse a signed BitValue
	@param bytes: the string containing the bitvalue
	@param nbits: the length of the bitvalue in bits
	@param offset: the offset of the bitvalue in the first byte
	"""
	
	result = 0
	
	total_bytes = len(bytes)
	padding_right = total_bytes*8 - nbits - offset
	
	# first byte, may be only partly significant
	byte = ord(bytes[0])
	mask = (1 << (8 - offset)) - 1
	bits = (byte & mask) << (nbits - (8 - offset))
	result |= bits
	
	# bytes in the middle
	for x, byte in enumerate(map(ord, bytes[1:-1])):
		bits = byte << (x+1)*8 - padding_right 
		result |= bits
	
	# last byte, may be only partly significant
	byte = ord(bytes[-1])
	bits = byte >> padding_right
	result |= bits 

	return result
		
def parse_int(bytes, little_endian=True):
	"""byte string to unsigned int"""
	if not little_endian:
		bytes = bytes[::-1]
		
	result = 0
	shift = 0
	for byte in bytes:
		result += ord(byte) << shift
		shift += 8
	
	return result
	

if __name__ == '__main__':
	try:
		path = sys.argv[1]
	except IndexError:
		sys.stderr.write("You must specify a path!\nUsage: ./swfinfo.py /path/to/file.swf\n")
		sys.exit(1)
	result = analyze(path)
	print "SWFInfo 0.1, Hannes Struß <x@hannesstruss.de>"
	print path
	for key in RESULT_FIELDS:
		print "%s: %s" % (key, result[key])