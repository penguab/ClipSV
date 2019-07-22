#!/usr/bin/env python	
import sys,re
	
def event_sv(bam):
	out_file=open(bam+".sv","w")	
	with open(bam) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			if re.match(r"^@",l):continue
			line=l.split('\t')
			if int(line[1])%512>=256 or int(line[1])>=2048: continue
			x=re.match(r"^NODE_\d*_length_\d*_cov_\d*\.\d*_HPall_(.*)_(.*)_(.*)_(.*)_(.*)_\d+$",line[0])
			if not x: continue
			chro=x.group(1)
			start=x.group(2)
			end=x.group(3)
			event=x.group(4)
			length=x.group(5)
			if line[2]!=chro or abs(int(line[3])-int(start))>=5000 or  abs(int(line[3])-int(end))>=5000: continue
			pos= line[3]
			cigar= line[5]
			mark=0
			while True:
				m=re.match(r'^(\d+)([A-Za-z])',cigar)
				if not m: break
				if int(m.group(1))>=30 and (m.group(2)=="D" or m.group(2)=="N" or m.group(2)=="I") and (int(pos)-int(start)>=-100 and int(pos)-int(end)<=100):
					if (m.group(2)=="D" or  m.group(2)=="N") and event=="DEL" and int(m.group(1))/int(length)>=0.5 and int(m.group(1))/int(length)<=2:
						out_file.write("\t".join([chro,start,str(int(start)+int(m.group(1))+1),"DEL",m.group(1),l])+"\n")
					elif m.group(2)=="I" and event=="INS" :
						out_file.write("\t".join([chro,start,str(int(start)+1),"INS",m.group(1),l])+"\n")
					elif (m.group(2)=="D" or  m.group(2)=="N") and event=="BND":
						out_file.write("\t".join([chro,start,str(int(start)+int(m.group(1))+1),"DEL",m.group(1),l])+"\n")
					elif m.group(2)=="I" and event=="BND":
						out_file.write("\t".join([chro,start,str(int(start)+1),"INS",m.group(1),l])+"\n")
					mark=1
				if m.group(2)=="M" or m.group(2)=="D":
					pos=str(int(pos)+int(m.group(1)))
				cigar=cigar[len(m.group(0)):]
			if mark==1: continue
			p=re.match(r"^(\d+)[SH].*M$",line[5])
			q=re.match(r"^\d+M.*(\d+)[SH]$",line[5])
			if int(line[3])-int(end)>100 or int(pos)-int(start)<-100:
				out_file.write ("\t".join(["-","-","-","no_event","-",l])+"\n")
			elif p and int(p.group(1))>=30 and (int(line[3])-int(start)>=-100 and int(line[3])-int(end)<=100):
				out_file.write ("\t".join([chro,start,str(int(start)+1),"right_boundary","-",l])+"\n")
			elif q and int(q.group(1))>=30 and (int(pos)-int(start)>=-100 and int(pos)-int(end)<=100):
				out_file.write ("\t".join([chro,start,str(int(start)+1),"left_boundary","-",l])+"\n")
			else:
				out_file.write ("\t".join(["-","-","-","wrong_assembly","-",l])+"\n")
	
	
