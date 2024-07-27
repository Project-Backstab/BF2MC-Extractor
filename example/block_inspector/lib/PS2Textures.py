import numpy as np

gsmem = [0] * (1024 * 1024)

block32 = [
	0,  1,  4,  5, 16, 17, 20, 21,
	2,  3,  6,  7, 18, 19, 22, 23,
	8,  9, 12, 13, 24, 25, 28, 29,
	10, 11, 14, 15, 26, 27, 30, 31
]

column_word_32 = [
	0,  1,  4,  5,  8,  9, 12, 13,
	2,  3,  6,  7, 10, 11, 14, 15
]

def write_tex_psmct32(dbp, dbw, dsax, dsay, rrw, rrh, data):
	index = 0
	startBlockPos = dbp * 64

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			pageX = x // 64
			pageY = y // 32
			page = pageX + pageY * dbw

			px = x - (pageX * 64)
			py = y - (pageY * 32)

			blockX = px // 8
			blockY = py // 8
			block = block32[blockX + blockY * 8]

			bx = px - blockX * 8
			by = py - blockY * 8

			column = by // 2

			cx = bx
			cy = by - column * 2
			cw = column_word_32[cx + cy * 8]
			
			gsmem[startBlockPos + (page * 2048) + (block * 64) + (column * 16) + cw] = data[index:index+4]
			index += 4
			
			## Debug
			
			print("startBlockPos = {}".format(startBlockPos))
			print("x = {}".format(x))
			print("y = {}".format(y))
			print("pageX = {}".format(pageX))
			print("pageY = {}".format(pageY))
			print("page = {}".format(page))
			print("px = {}".format(px))
			print("py = {}".format(py))
			print("blockX = {}".format(blockX))
			print("blockY = {}".format(blockY))
			print("block = {}".format(block))
			print("bx = {}".format(bx))
			print("by = {}".format(by))
			print("column = {}".format(column))
			print("cx = {}".format(cx))
			print("cy = {}".format(cy))
			print("cw = {}".format(cw))
			print("gsmem = {}".format(int.from_bytes(gsmem[startBlockPos + (page * 2048) + (block * 64) + (column * 16) + cw], 'little')))
			print("--------------------------------")
			
	
	return gsmem

def read_tex_psmct32(dbp, dbw, dsax, dsay, rrw, rrh):
	result = np.zeros(rrw * rrh, dtype=np.uint32)
	dest = iter(result)
	start_block_pos = dbp * 64

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			page_x = x // 64
			page_y = y // 32
			page = page_x + page_y * dbw

			px = x - (page_x * 64)
			py = y - (page_y * 32)

			block_x = px // 8
			block_y = py // 8
			block = block32[block_x + block_y * 8]

			bx = px - block_x * 8
			by = py - block_y * 8

			column = by // 2

			cx = bx
			cy = by - column * 2
			cw = column_word_32[cx + cy * 8]

			dest_value = gsmem[start_block_pos + page * 2048 + block * 64 + column * 16 + cw]
			dest.send(dest_value)

	return result

block8 = [
	0, 1, 4, 5, 16, 17, 20, 21,
	2, 3, 6, 7, 18, 19, 22, 23,
	8, 9, 12, 13, 24, 25, 28, 29,
	10, 11, 14, 15, 26, 27, 30, 31
]

column_word_8 = [
	[
		0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13,
		2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15,
		8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5,
		10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7
	],
	[
		8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5,
		10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7,
		0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13,
		2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15
	]
]

column_byte_8 = [
	0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
	0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
	1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
	1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3
]

def write_tex_psmt8(dbp, dbw, dsax, dsay, rrw, rrh, data):
	dbw //= 2
	src = iter(data)
	start_block_pos = dbp * 64

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			page_x = x // 128
			page_y = y // 64
			page = page_x + page_y * dbw

			px = x - (page_x * 128)
			py = y - (page_y * 64)

			block_x = px // 16
			block_y = py // 16
			block = block8[block_x + block_y * 8]

			bx = px - block_x * 16
			by = py - block_y * 16

			column = by // 4

			cx = bx
			cy = by - column * 4
			cw = column_word_8[column % 2][cx + cy * 16]
			cb = column_byte_8[cx + cy * 16]

			dst = gsmem[start_block_pos + page * 2048 + block * 64 + column * 16 + cw]

			dst[cb] = next(src)

def read_tex_psmt8(dbp, dbw, dsax, dsay, rrw, rrh):
	dbw >>= 1
	startBlockPos = dbp * 64
	result = []

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			pageX = x // 128
			pageY = y // 64
			page = pageX + pageY * dbw

			px = x - (pageX * 128)
			py = y - (pageY * 64)

			blockX = px // 16
			blockY = py // 16
			block = block8[blockX + blockY * 8]

			bx = px - blockX * 16
			by = py - blockY * 16

			column = by // 4

			cx = bx
			cy = by - column * 4
			cw = column_word_8[column & 1][cx + cy * 16]
			cb = column_byte_8[cx + cy * 16]

			result.append(gsmem[startBlockPos + (page * 2048) + (block * 64) + (column * 16) + cw][cb])
			
			## Debug
			
			print("startBlockPos = {}".format(startBlockPos))
			print("x = {}".format(x))
			print("y = {}".format(y))
			print("pageX = {}".format(pageX))
			print("pageY = {}".format(pageY))
			print("page = {}".format(page))
			print("px = {}".format(px))
			print("py = {}".format(py))
			print("blockX = {}".format(blockX))
			print("blockY = {}".format(blockY))
			print("block = {}".format(block))
			print("bx = {}".format(bx))
			print("by = {}".format(by))
			print("column = {}".format(column))
			print("cx = {}".format(cx))
			print("cy = {}".format(cy))
			print("cw = {}".format(cw))
			print("gsmem = {}".format(gsmem[startBlockPos + (page * 2048) + (block * 64) + (column * 16) + cw][cb]))
			print("--------------------------------")
			
	
	return result

block4 = [
	0, 2, 8, 10,
	1, 3, 9, 11,
	4, 6, 12, 14,
	5, 7, 13, 15,
	16, 18, 24, 26,
	17, 19, 25, 27,
	20, 22, 28, 30,
	21, 23, 29, 31
]

column_word_4 = [
	[
		0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13,
		0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13,
		2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15,
		2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15
	],
	[
		8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5,
		8, 9, 12, 13, 0, 1, 4, 5, 8, 9, 12, 13, 0, 1, 4, 5,
		10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7,
		10, 11, 14, 15, 2, 3, 6, 7, 10, 11, 14, 15, 2, 3, 6, 7
	]
]

column_byte_4 = [
	0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
	4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
	4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6,
	1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
	5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7,
	1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3,
	5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7
]

def write_tex_psmt4(dbp, dbw, dsax, dsay, rrw, rrh, data):
	dbw //= 2
	src = iter(data)
	start_block_pos = dbp * 64
	odd = False

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			page_x = x // 128
			page_y = y // 128
			page = page_x + page_y * dbw

			px = x - (page_x * 128)
			py = y - (page_y * 128)

			block_x = px // 32
			block_y = py // 16
			block = block4[block_x + block_y * 4]

			bx = px - block_x * 32
			by = py - block_y * 16

			column = by // 4

			cx = bx
			cy = by - column * 4
			cw = column_word_4[column % 2][cx + cy * 32]
			cb = column_byte_4[cx + cy * 32]

			dst = gsmem[start_block_pos + page * 2048 + block * 64 + column * 16 + cw]

			if cb & 1:
				if odd:
					dst = (dst & 0x0F) | (next(src) & 0xF0)
				else:
					dst = (dst & 0xF0) | ((next(src) << 4) & 0xF0)
			else:
				if odd:
					dst = (dst & 0x0F) | ((next(src) >> 4) & 0x0F)
				else:
					dst = (dst & 0xF0) | (next(src) & 0x0F)

			odd = not odd
			gsmem[start_block_pos + page * 2048 + block * 64 + column * 16 + cw] = dst

def read_tex_psmt4(dbp, dbw, dsax, dsay, rrw, rrh):
	dbw //= 2
	result = []
	start_block_pos = dbp * 64
	odd = False

	for y in range(dsay, dsay + rrh):
		for x in range(dsax, dsax + rrw):
			page_x = x // 128
			page_y = y // 128
			page = page_x + page_y * dbw

			px = x - (page_x * 128)
			py = y - (page_y * 128)

			block_x = px // 32
			block_y = py // 16
			block = block4[block_x + block_y * 4]

			bx = px - block_x * 32
			by = py - block_y * 16

			column = by // 4

			cx = bx
			cy = by - column * 4
			cw = column_word_4[column % 2][cx + cy * 32]
			cb = column_byte_4[cx + cy * 32]

			src = gsmem[start_block_pos + page * 2048 + block * 64 + column * 16 + cw]

			if cb & 1:
				if odd:
					result.append(src & 0xF0)
				else:
					result.append((src >> 4) & 0x0F)
			else:
				if odd:
					result.append((src << 4) & 0xF0)
				else:
					result.append(src & 0x0F)

			odd = not odd

	return result