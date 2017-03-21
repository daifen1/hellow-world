def readIges(filePath,DotList):
	file=open(filePath,'r+')
	for line in file.readlines():
		data=line[:80]
		id_code=line[72]
		if id_code=='P':
			line=line.split(',')
			dot=[float(line[1]),float(line[2]),float(line[3])]
			DotList.append(dot)
			#print float(line[1]),float([line[2]]),float([line[3]])
			#DotList.append([float(line[1]),float(line[2]),float(line[3])
	file.close()
if __name__=='__main__':
	filePath="C:/Users/wu/Documents/catia/lineDot.IGS"
	DotList=[]
	readIges(filePath, DotList)
	for dot in DotList:
		print dot,type(dot[0])

#[float(dot[0]),float(dot[1]),float(dot[2])]