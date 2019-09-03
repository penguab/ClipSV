#!/usr/bin/env python	
import os,shutil,subprocess,sys,re
def genotype(name,bam,min_insert_size,max_insert_size):	
	out_file=open(name.split(".")[0]+".genotype.vcf",'w')
	match_p=re.compile(r'^(\d+)([MDISH])')
	with open (name) as f:
		while True:
			l=f.readline().rstrip()
			if not l: break
			if l[0]=="#":
				out_file.write(l+"\n")
				continue
			line=l.split("\t")
			del_p=re.search(r'SVTYPE=DEL',line[7])
			cov_para=line[0]+":"+str(int(line[1])-100)+"-"+str(int(line[1])-50)
			devnull=open(os.devnull, 'w')
			cov_command= subprocess.Popen(['samtools','depth',bam,'-r',cov_para], stdout=subprocess.PIPE,stderr=devnull)
			cov_total,cov_number=0,0
			while True:
				sam= cov_command.stdout.readline().decode('utf-8').rstrip()
				if not sam: break
				cont=sam.split('\t')
				cov_total+=int(cont[-1])
				cov_number+=1
			if cov_number==0:
				coverage=-1
			else:
				coverage=float(cov_total)/cov_number
			cov_command.communicate()
			para=line[0]+":"+str(int(line[1])-20)+"-"+str(int(line[1])+80)
			command= subprocess.Popen(['samtools','view',bam,para], stdout=subprocess.PIPE,stderr=devnull)
			clip=0
			normal=0
			while True:
				sam= command.stdout.readline().decode('utf-8').rstrip()
				if not sam: break
				cont=sam.split('\t')
				cigar=cont[5]
				pos= cont[3]
				while True:
					m=match_p.search(cigar)
					if not m: break
					if m.group(2)=="M" or m.group(2)=="D":
						pos=str(int(pos)+int(m.group(1)))
					cigar=cigar[len(m.group(0)):]
				m1=re.search(r'[SH]',cont[5])
				if m1:
					clip+=1
				elif int(cont[3])-int(line[1])<-20 and int(pos)-int(line[1])>20:
					normal+=1
			command.communicate()
			if clip+normal==0:
				out_file.write(l+":CR:NR\t./.:0:0\n")
			elif del_p:
				if clip>=3 and normal>=3:
					out_file.write(l+":CR:NR\t0/1:"+str(clip)+":"+str(normal)+"\n")
				elif float(clip)/float(clip+normal)>=0.2 and float(clip)/float(clip+normal)<=0.8:
					out_file.write(l+":CR:NR\t0/1:"+str(clip)+":"+str(normal)+"\n")
				elif float(clip)/float(clip+normal)>0.8 or float(clip)/coverage >=1:
					out_file.write(l+":CR:NR\t1/1:"+str(clip)+":"+str(normal)+"\n")
				else:
					out_file.write(l+":CR:NR\t./.:"+str(clip)+":"+str(normal)+"\n")
			else:
				if float(clip)/float(clip+normal)>0.8 or float(clip)/coverage >=1:
					out_file.write(l+":CR:NR\t1/1:"+str(clip)+":"+str(normal)+"\n")
				elif float(clip)/float(clip+normal)>=0.2 and float(clip)/float(clip+normal)<=0.8:
					out_file.write(l+":CR:NR\t0/1:"+str(clip)+":"+str(normal)+"\n")
				else:
					out_file.write(l+":CR:NR\t./.:"+str(clip)+":"+str(normal)+"\n")

if __name__=="__main__"	:
	[name,bam,min_insert_size,max_insert_size]=sys.argv[1:]
	genotype(name,bam,min_insert_size,max_insert_size)

