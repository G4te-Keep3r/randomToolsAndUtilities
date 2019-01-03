import os, sys, time, hashlib, io, shutil

fileInfo = {}

#M:\twitch\toCompare

def sha512(src, length=io.DEFAULT_BUFFER_SIZE):
	sha512 = hashlib.sha512()
	with io.open(src, mode="rb") as fd:
		for chunk in iter(lambda: fd.read(length), b''):
			sha512.update(chunk)
	return sha512

def sha256(src, length=io.DEFAULT_BUFFER_SIZE):
	sha256 = hashlib.sha256()
	with io.open(src, mode="rb") as fd:
		for chunk in iter(lambda: fd.read(length), b''):
			sha256.update(chunk)
	return sha256

#not working, just gonna use 2 sha 512 and 256
def blake2b(src, length=io.DEFAULT_BUFFER_SIZE):
	blake2b = hashlib.blake2b()
	with io.open(src, mode="rb") as fd:
		for chunk in iter(lambda: fd.read(length), b''):
			blake2b.update(chunk)
	return blake2b

def md5sum(src, length=io.DEFAULT_BUFFER_SIZE):
	md5 = hashlib.md5()
	with io.open(src, mode="rb") as fd:
		for chunk in iter(lambda: fd.read(length), b''):
			md5.update(chunk)
	return md5

def processFile(fname, f):
	fileInfo[fname][0].append(os.path.getsize(f))
	fileInfo[fname][1].append(md5sum(f).hexdigest())
	fileInfo[fname][2].append(sha512(f).hexdigest())
	fileInfo[fname][3].append(sha256(f).hexdigest())
	fileInfo[fname][3].append(f)

def main():
	drives = ['M:\\twitch\\toCompare\\']
	delDir = 'M:\\twitch\\delete\\'

	totalCount = 0
	uniqueCount = 0
	errFiles = 0

	for walk_dir in drives:
		#print '#####'
		#print 'starting', walk_dir
		for root, subdirs, files in os.walk(walk_dir):
			for f in files:
				print totalCount,
				'''
				print
				print os.path.join(root, f)
				print os.path.join('M:\\twitch\\delete\\', f)
				print
				print root
				print
				print f
				print
				return
				'''
				try:
					fname = f.split('.mp4')#[0]
					fname = fname[0]
					if fname[-1] == ')':
						fname = fname[:-4] #remove ' (#)'
					if fname not in fileInfo:
						fileInfo[fname] = [[], [], [], [], []] #size, md5, sha512, sha256, f (to move the ones with () in them)
						uniqueCount += 1
					processFile(fname, os.path.join(root, f))
					totalCount += 1

				except Exception, e:
					errFiles += 1
					print '********', f
					pass
		#print '#####*'
		#print 'done with drive', walk_dir
		print '#####*#'
		print 'total errFiles:', errFiles
		print 'total files:', totalCount
		print 'uniqueCount:', uniqueCount
		print '#####*##'
		print '#####*##*#####'
		print '\n\n\n'

	print '='*24
	print
	for fname in fileInfo:
		print fname
		print fileInfo[fname][0]
		print fileInfo[fname][1]
		print fileInfo[fname][2]
		print fileInfo[fname][3]
		print
	print '='*24
	print
	print
	print 'check if files are dupes'
	print
	good = 0
	bad = 0
	numToDelete = 0
	numToSave = 0
	numMoved = 0
	numLeft = 0
	for fname in fileInfo:
		print fname, 'files: '+str(len(fileInfo[fname][0]))
		size = True
		if len(fileInfo[fname][0]) > 1:
			for i in fileInfo[fname][0][1:]:
				size = size and i==fileInfo[fname][0][0]
			md5 = True
			for i in fileInfo[fname][1][1:]:
				md5 = md5 and i==fileInfo[fname][1][0]
			sha512 = True
			for i in fileInfo[fname][2][1:]:
				sha512 = sha512 and i==fileInfo[fname][2][0]
			sha256 = True
			for i in fileInfo[fname][3][1:]:
				sha256 = sha256 and i==fileInfo[fname][3][0]
			print size, md5, sha512, sha256
			if size and md5 and sha512 and sha256:
				print 'they match :)'
				numToSave += 1
				numToDelete += len(fileInfo[fname][0]) - 1
				#move the extra copies to delDir
				resString = ''
				for f in fileInfo[fname][4]:
					if '(' in f:
						shutil.move(os.path.join(drives[0], f), os.path.join(delDir, f))
						print f, 'moved'
						resString += '#'
						numMoved += 1
					else:
						print f, 'left wheere is'
						resString += '*'
						numLeft += 1
				print resString
			else:
				print
				print
				print '-/-*/-*/'*5
				print
				print
			print
		else:
			numToSave += 1
	print
	print 'uniqueCount:', uniqueCount, 'numToSave:', numToSave, uniqueCount==numToSave
	print
	print 'numToSave:', numToSave, 'numLeft:', numLeft, numToSave==numLeft
	print 'numToDelete:', numToDelete, 'numMoved:', numMoved, numToDelete==numMoved

if __name__ == '__main__':
	main()