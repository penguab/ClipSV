#!/usr/bin/env python	
import sys,re
	
def minimap2_sv(minimap2_out):
	out=open(minimap2_out+'.sv','w')	
	with open(minimap2_out) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			if l[0]=='@':continue
			line=l.split('\t')
			if int(line[1])%512>=256 or int(line[1])>=2048 or int(line[4])<10 : continue
			p=re.search(r'^(\d+)M.*\D(\d+)M$',line[5])
			if not p: continue
			if int(p.group(1))<20 or int(p.group(2))<20:
				continue
			pos= line[3]
			cigar= line[5]
			mark=0
			while True:
				m=re.match(r'^(\d+)([A-Za-z])',cigar)
				if not m: break
				if int(m.group(1))>=5 and (m.group(2)=="D" or m.group(2)=="N" or m.group(2)=="I") :
					if (m.group(2)=="D" or  m.group(2)=="N") :
						out.write('\t'.join([line[2],pos,str(int(pos)+int(m.group(1))+1),"DEL",m.group(1),l])+'\n')
					elif m.group(2)=="I" :
						out.write('\t'.join([line[2],pos,str(int(pos)+1),"INS",m.group(1),l])+'\n')
				if m.group(2)=="M" or m.group(2)=="D":
					pos=str(int(pos)+int(m.group(1)))
				cigar=cigar[len(m.group(0)):]
	
if __name__=='__main__':
	minimap2_sv(sys.argv[1])
	
