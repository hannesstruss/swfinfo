#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import swfinfo

if __name__ == '__main__':
	result = swfinfo.analyze(sys.argv[1])
	print swfinfo.format(result)
