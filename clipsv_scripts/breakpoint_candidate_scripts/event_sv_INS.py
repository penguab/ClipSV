#!/usr/bin/env python	
import sys,re
	
def event_sv_INS(event_sv):
	out_file=open(event_sv+'.INS','w')
	info=[]
	total=[]
	with open(event_sv) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			m=re.search(r'.*HPall_([^-]*)-*',line[5])
			if not m:
				continue
			if line[3]=="INS" or line[3]=="left_boundary" or line[3]=="right_boundary":
				if line[4]=='-':
					info.append([line[0],line[1],line[2],"INS",'0',m.group(1)])
				else:
					info.append([line[0],line[1],line[2],"INS",line[4],m.group(1)])
	info_sorted=sorted(info,key=lambda x: (x[5],-int(x[4])))
	mark={}
	for i in range(len(info_sorted)):
		name=info_sorted[i][5]
		if not name in mark:
			if info_sorted[i][4]=='0':
				total.append(info_sorted[i][0:4]+['-'])
			else:
				total.append(info_sorted[i][0:5])
		mark[name]=1
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1]),int(x[2])))
	pre='0'
	for x in range(len(total_sorted)):
		if int(total_sorted[x][1])>int(pre):
			out_file.write("\t".join(total_sorted[x])+"\n")
		pre=total_sorted[x][2]

if __name__=='__main__':
	event_sv_INS(sys.argv[1])

