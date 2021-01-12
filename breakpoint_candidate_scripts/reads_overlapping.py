#!/home/pengxu/.conda/envs/python3/bin/python
	
import subprocess,sys,re
	
def reads_overlapping(candidate_clips):	
	out_file=open(candidate_clips+"_overlapping","w")
	def overlap(left,right):
		contig=''
		index_left=-1
		index_right=-1
		for n in reversed(range(0,len(left)-30)):
			kmer=left[n:len(left)]
			occur=right.find(kmer)
			if occur==-1:
				break
			else:
				index_left = n
				index_right = occur
		if index_right !=-1 and index_right <=3:
			contig=left[0:index_left]+right[index_right:]
		return contig
			
	pre_chrom,pre_end='',0
	match_p=re.compile(r'^(\d+)([MDI])')
	left_p=re.compile(r'^(\d+)M(\d+[MDI])*(\d+)[S]$')
	right_p=re.compile(r'^(\d+)[S](\d+[MDI])*(\d+)M$')
	array=[]
	with open(candidate_clips) as f:
		while True:
			l=f.readline().rstrip()
			if not l:break
			if l[0]=='@': continue
			line=l.split('\t')
			if int(line[1])>=2048 or int(line[1])%2048>=1024 or int(line[1])%512>=256: continue
			if int(line[4])<20: continue
			left=left_p.search(line[5])
			right=right_p.search(line[5])
			if not left:
				if not right: continue
			cigar=line[5]
			pos= line[3]
			while True:
				m=match_p.search(cigar)
				if not m: break
				if m.group(2)=="M" or m.group(2)=="D":
					pos=str(int(pos)+int(m.group(1)))
				cigar=cigar[len(m.group(0)):]
			if pre_chrom=='' and left:
				pre_chrom=line[2]
				pre_end=int(pos)
				array=[line[9]]
			elif pre_chrom=='' and right:
				continue
			if line[2]==pre_chrom and int(line[3])<pre_end+1000:
				if left:
					array.append(line[9])
					pre_end=int(pos)
				elif right:
					for i in range(len(array)):
						contig=overlap(array[i],line[9])
						if not contig: continue
						out_file.write('>'+pre_chrom+'_'+str(pre_end)+'\n'+contig+'\n')
			elif line[2]!=pre_chrom or int(line[3])>=pre_end+1000:
				if left:
					pre_chrom=line[2]
					pre_end=int(pos)
					array=[line[9]]

if __name__ == "__main__":
	candidate_clips=sys.argv[1]
	reads_overlapping(candidate_clips)


