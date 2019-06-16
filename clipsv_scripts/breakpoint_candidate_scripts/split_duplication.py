#!/usr/bin/env python
def split_duplication(split):
	out_file=open(split+".duplication","w")
	total=[]
	left,riht={},{}
	with open(split) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if int(line[9])<60:
				continue
			if int(line[6])%256>=128:
				read="R2"
			elif int(line[6])%128>=64:
				read="R1"
			name=line[5]+"\t"+read+"\t"+line[3]
			if name in left:
				cont=left[name].split('\t')
				left.pop(line[5], None)
				num1,direction1=cont[4].split(':')
				num2,direction2=line[4].split(':')
				attach=['0']*7
				for i in range(len(attach)):
					attach[i]=str(int(cont[17+i])+int(line[17+i]))
				if line[0]==cont[0] and direction1=='left' and direction2=='right':
					total.append([cont[0],cont[1],line[1],cont[3]]+cont[5:15]+line[5:15]+attach)
				elif line[0]==cont[0] and direction1=='right' and direction2=='left':
					total.append([cont[0],line[1],cont[1],cont[3]]+line[5:15]+cont[5:15]+attach)
			else:
				left[name]=l
	total_filter=[]
	for i in total:
		if int(i[2])-int(i[1])<=-40:
			total_filter.append([i[0],i[2],i[1]]+i[3:])
	total_sorted=sorted(total_filter,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
	
	
	
