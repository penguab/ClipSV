#!/usr/bin/env python	
import sys,re
	
def translocation_site(large_insertion):
	out_file=open(large_insertion+'.site','w')	
	total=[]
	left_p=re.compile(r'^(\d+)M(\d+[MDI])*(\d+)[SH]$')
	match_p=re.compile(r'^(\d+)([MDISH])')
	with open(large_insertion) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			line=l.split('\t')
			if line[15][0:4]=="SA:Z":
				cigar=line[15].split(",")[3]
				chro2=line[15].split(",")[0][5:]
				if chro2 != line[0] and chro2 != line[11]: continue
				pos=line[15].split(",")[1]
				left=left_p.search(cigar)
				if left:
					while True:
						m=match_p.search(cigar)
						if not m: break
						if m.group(2)=="M" or m.group(2)=="D":
							pos=str(int(pos)+int(m.group(1)))
						cigar=cigar[len(m.group(0)):]	
				total.append([line[0],line[1],line[3],chro2,pos,"split"])
			else:
				total.append([line[0],line[1],line[3],line[11],line[12],"discordant"])
	total_sorted=sorted(total,key=lambda x: (x[0], int(x[1]),x[3],int(x[4])))
	for x in range(len(total_sorted)):
		out_file.write(('\t'.join(str(n) for n in total_sorted[x]))+'\n')
	
if __name__ =="__main__":
	translocation_site(sys.argv[1])
