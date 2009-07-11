# -*- coding: utf-8 -*-

from __future__ import with_statement

import math
import zlib

def analyze(path):
	result = {}
	with open(path, "rb") as file_obj:
		buffer = file_obj.read(8)
		
		compressed = buffer[0] == "C"
		
		result["Compressed"] = "yes" if compressed else "no"
		result["Version"] = ord(buffer[3])
		result["Uncompressed Size"] = parse_int(buffer[4:8])
		
		compressed_content = file_obj.read()
		
		result["Compressed Size"] = len(compressed_content) + 8
		
		uncompressed_content = zlib.decompress(compressed_content)
		
		result["Stage Dimensions"] = parse_rect(file_obj, 8)
		
		return result

def parse_rect(file_obj, index):
	"""
	parses a RECT structure.
	@param file_obj: a file object that supports seek
	@param index: the index of the nbits of the RECT
	@return: a tuple, (width, height) 
	"""
	result = []

	file_obj.seek(index)
	nbits = ord(file_obj.read(1)) >> 3
	rect_len = int(math.ceil((nbits * 4 + 5) / 8.0)) # number of bytes the rect needs, including nbits
	
	file_obj.seek(index)
	buffer = file_obj.read(rect_len)
	offset = 5
	for n in xrange(4): # read 4 bitvalues
		first_byte = offset / 8
		bitval_length = int(math.ceil(((offset % 8) + nbits) / 8.0))
		result.append(parse_SB(
			buffer[first_byte:][:bitval_length], 
			nbits, 
			offset % 8))
		
		offset += nbits
	
	return tuple(result)
	
#
# !.......!.......!.......!.......
#                         #######################
#
#

	
def parse_SB(bytes, nbits, offset):
	"""
	parse a signed BitValue
	@param bytes: the string containing the bitvalue
	@param nbits: the length of the bitvalue in bits
	@param offset: the offset of the bitvalue in the first byte
	"""
	
	result = 0
	padding_left = 8 - offset
	
	result = result | ord(bytes[0]) << (nbits - padding_left)
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
	print analyze("/home/hannes/Desktop/FUUU.swf")