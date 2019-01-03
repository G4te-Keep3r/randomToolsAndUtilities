import os, sys, time, hashlib, io

fileInfo = {}

#M:\twitch\toCompare
#M:\twitch\delete

def main():
	drives = ['M:\\twitch\\toCompare\\', 'M:\\twitch\\delete\\']

	totalCount = [0, 0]
	uniqueCount = [0, 0]
	errFiles = [0, 0]

	for walk_dir_index in range(len(drives)):
		walk_dir = drives[walk_dir_index]
		print '#####'
		print 'starting', walk_dir
		for root, subdirs, files in os.walk(walk_dir):
			for f in files:
				print totalCount,
				try:
					fname = f.split('.mp4')#[0]
					fname = fname[0]
					if fname[-1] == ')':
						fname = fname[:-4] #remove ' (#)'
					if fname not in fileInfo:
						fileInfo[fname] = [0, 0] #toCompare, delete
						uniqueCount[walk_dir_index] += 1
					#processFile(fname, os.path.join(root, f))
					fileInfo[fname][walk_dir_index] += 1
					totalCount[walk_dir_index] += 1

				except Exception, e:
					errFiles[walk_dir_index] += 1
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
		print fileInfo[fname]
		print
	print '='*24
	print
	print
	print 'check if files are dupes'
	print
	numToDelete = 0
	numToSave = 0
	for fname in fileInfo:
		print fname, 'files: '+str(sum(fileInfo[fname]))
		numToSave += fileInfo[fname][0] #should be 1 every time
		numToDelete += fileInfo[fname][1]
		print
	print
	print 'uniqueCount:', uniqueCount, 'numToSave:', numToSave, uniqueCount==numToSave
	print
	print 'numToSave:', numToSave
	print 'numToDelete:', numToDelete
	print
	print
	for fname in fileInfo:
		print fileInfo[fname]
	print
	print
	print
	for fname in fileInfo:
		print '['+('*'*fileInfo[fname][0])+', '+('*'*fileInfo[fname][1])+']'

if __name__ == '__main__':
	main()