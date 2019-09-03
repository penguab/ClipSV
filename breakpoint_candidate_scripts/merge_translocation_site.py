#!/usr/bin/env python	
import sys,re
	
def merge_translocation_site(translocation,fold):	
	out_file=open("translocation_total","w")
	def comp(para1,para2,discordant):
		line=para1.split('\t')
		inside,overlap=0,0
		for i in range(len(para2)):
			region=para2[i].split('\t')
			if line[0]==region[0] and line[2]==region[2] and int(line[1])-int(region[1])<=20 and abs(int(line[3])-int(region[3]))<=20:
				region[1]=line[1]
				if int(line[3])-int(region[3])>0: 
					region[3]=line[3]
				for m in range(4,5):
					region[m]=str(int(region[m])+int(line[m]))
				para2[i]='\t'.join(region)
				inside=1
				break
			elif line[0]==region[0] and line[2]==region[2] and int(line[1])-int(region[1])<=20 and abs(int(line[3])-int(region[3]))>20:
				overlap=1
			elif line[0]==region[0] and line[2]!=region[2] and int(line[1])-int(region[1])<=20:
				overlap=1
		if inside==0 and overlap==1:
			para2.append(para1)
		elif inside==0 and overlap==0:
			for x in range(len(para2)):
				out=para2[x].split('\t')
				if int(out[4])>=int(fold)-1:
					total=0
					for y in range(len(discordant)):
						if out[0]==discordant[y][0] and out[2]==discordant[y][2] and abs(int(out[1])-int(discordant[y][1]))<=1000 and abs(int(out[3])-int(discordant[y][3]))<=1000:
							total=total+1
					if int(out[4])+total>=2*(int(fold)-1):
						out_file.write("\t".join([out[0],out[1],str(int(out[1])+1),"TRANS",out[2]+":"+out[3],out[4],str(total)])+"\n")
			para2=[para1]
		return para2
	
	left,right=[],[]
	discordant=[]
	with open(translocation) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[-1]=="discordant":
				discordant.append([line[0],line[1],line[3],line[4]])


	with open(translocation) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			if line[-1]=="discordant":
				continue
			cont='\t'.join([line[0],line[1],line[3],line[4],'1'])
			if line[2]=='hp1':
				if len(left)==0:
					left=[cont]
					continue
				left=comp(cont,left,discordant)
			elif line[2]=='hp2':
				if len(right)==0:
					right=[cont]
					continue
				right=comp(cont,right,discordant)
	
	for x in range(len(left)):
		out=left[x].split('\t')
		if int(out[4])>=int(fold)-1:
			total=0
			for y in range(len(discordant)):
				if out[0]==discordant[y][0] and out[2]==discordant[y][2] and abs(int(out[1])-int(discordant[y][1]))<=1000 and abs(int(out[3])-int(discordant[y][3]))<=1000:
					total=total+1
			if int(out[4])+total>=2*(int(fold)-1):
				out_file.write("\t".join([out[0],out[1],str(int(out[1])+1),"TRANS",out[2]+":"+out[3],out[4],str(total)])+"\n")
	for x in range(len(right)):
		out=right[x].split('\t')
		if int(out[4])>=int(fold)-1:
			total=0
			for y in range(len(discordant)):
				if out[0]==discordant[y][0] and out[2]==discordant[y][2] and abs(int(out[1])-int(discordant[y][1]))<=1000 and abs(int(out[3])-int(discordant[y][3]))<=1000:
					total=total+1
			if int(out[4])+total>=2*(int(fold)-1):
				out_file.write("\t".join([out[0],out[1],str(int(out[1])+1),"TRANS",out[2]+":"+out[3],out[4],str(total)])+"\n")

if __name__=="__main__":
	merge_translocation_site(sys.argv[1],sys.argv[2])

	
