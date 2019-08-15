#!/usr/bin/env python
import sys,re

def split_inversion(split):
	out_file=open(split+".inversion","w")
	total=[]
	left,riht={},{}
	with open(split) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if int(line[9])<0:
				continue
			if line[15][0:2]=="SA":
				sa=line[15].split(",")
				m=re.search(r'^\d+[SH](\d+)M\d+[SH]$',sa[3])
				if m:
					if (int(line[6])%32 >=16 and sa[2]=="+") or (int(line[6])%32 <16 and sa[2]=="-"):
						total.append([sa[0][5:],sa[1],str(int(sa[1])+int(m.group(1)))]+line[3:])
			if int(line[6])%256>=128:
				read="R2"
			elif int(line[6])%128>=64:
				read="R1"
			name=line[5]+"\t"+read+"\t"+line[3]
			if name in left:
				cont=left[name].split('\t')
				left.pop(line[5], None)
				if (int(cont[6])%32 >=16 and int(line[6])%32 >=16) or (int(cont[6])%32 <16 and int(line[6])%32 <16): continue
				num1,direction1=cont[4].split(':')
				num2,direction2=line[4].split(':')
				attach=['0']*7
				for i in range(len(attach)):
					attach[i]=str(int(cont[17+i])+int(line[17+i]))
				if line[0]==cont[0] and direction1=='left' and direction2=='left':
					total.append([cont[0],cont[1],line[1],cont[3]]+cont[5:15]+line[5:15]+attach)
				elif line[0]==cont[0] and direction1=='right' and direction2=='right':
					total.append([cont[0],cont[8],line[8],cont[3]]+line[5:15]+cont[5:15]+attach)
			else:
				left[name]=l
	total_filter=[]
	for i in total:
		if int(i[2])-int(i[1])>=40:
			total_filter.append(i)
	total_sorted=sorted(total_filter,key=lambda x: (x[0], int(x[1]),int(x[2])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
	
if __name__=='__main__':
	split_inversion(sys.argv[1])
	
