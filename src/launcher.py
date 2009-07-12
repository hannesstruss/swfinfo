# -*- coding: utf-8 -*-

import swfinfo

if __name__ == '__main__':
	result = swfinfo.analyze("../FUUU.swf")
	print swfinfo.format(result)