# -*- coding: utf-8 -*-

from __future__ import with_statement

def analyze(path):
	result = {}
	with open(path, "rb") as file_obj:
		headers = file_obj.read(100)
		
		result["Compressed"] = "yes" if headers[0] == "C" else "no"
		result["Version"] = ord(headers[3])
		result["Uncompressed Size"] = parse_int(headers[4:8])
		result["Stage Dimensions"] = parse_rect(headers[0xb:])
		
		return result

def parse_rect(bytes):
	"""
	parses a RECT structure. bytes must be long enough 
	"""
	nbits = ord(bytes[0]) >> 3
	print nbits

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