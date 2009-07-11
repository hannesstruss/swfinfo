# -*- coding: utf-8 -*-

def analyze(file_obj):
	result = {}
	headers = file_obj.read(100)
	
	result["Compressed"] = "yes" if headers[0] == "C" else "no"
	result["Version"] = ord(headers[3])
	result["Uncompressed Size"] = parse_int(headers[4:8])
	
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
	print analyze(open("/home/hannes/Desktop/FUUU.swf"))