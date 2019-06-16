#!/usr/bin/env python	
def merge_clips_deletion(clips_DEL):
	output=open(clips_DEL+".merge",'w')
	def comp(para1,para2):
		line=para1.split('\t')
		inside,overlap=0,0
		for i in range(len(para2)):
			region=para2[i].split('\t')
			if line[0]==region[0] and int(line[1])-int(region[1])<=20 and abs(int(line[2])-int(region[2]))<=20:
				region[1]=line[1]
				if int(line[2])-int(region[2])<0: 
					region[2]=line[2]
				for m in [4]:
					region[m]=str(int(region[m])+int(line[m]))
				para2[i]='\t'.join(region)
				inside=1
				break
			elif line[0]==region[0] and int(line[1])-int(region[1])<=20 and abs(int(line[2])-int(region[2]))>20:
				overlap=1
		if inside==0 and overlap==1:
			para2.append(para1)
		elif inside==0 and overlap==0:
			for x in range(len(para2)):
				out=para2[x].split('\t')
				output.write("\t".join([out[0],out[1],out[2],out[3],str(int(out[2])-int(out[1])),out[4]])+'\n')
			para2=[para1]
		return para2
	
	left=[]
	with open(clips_DEL) as f:
		while True:
			l= f.readline().rstrip()
			if not l: break
			line= l.split('\t')
			cont='\t'.join([line[0],line[1],line[2],line[3],line[5]])
			if line[3]=='DEL':
				if len(left)==0:
					left=[cont]
					continue
				left=comp(cont,left)
	
	for x in range(len(left)):
		out=left[x].split('\t')
		output.write("\t".join([out[0],out[1],out[2],out[3],str(int(out[2])-int(out[1])),out[4]])+'\n')
	
