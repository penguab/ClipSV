#!/usr/bin/env python
import subprocess,sys,re,os

def extract_breakpoints(chromosome,bam, genome, min_insert_size, max_insert_size,read_length):
	os.mkdir(chromosome+"_dir")
	os.chdir(chromosome+"_dir")
	left_p=re.compile(r'^(\d+)M(\d+[MDI])*(\d+)[SH]$')
	right_p=re.compile(r'^(\d+)[SH](\d+[MDI])*(\d+)M$')
	indel_p=re.compile(r'^\d+M(\d+\w)?\d+M$')
	whole_p=re.compile(r'^(\d+)(M)\d+[DIM](\d+[MDI])+(\d+)(M)$')
	match_p=re.compile(r'^(\d+)([MDISH])')
	MC_p=re.compile(r'MC:Z:([^\t]+)')
	XA_p=re.compile(r'XA:Z:([^,]+),[-+]([^,]+),([^,]+),[^\t]+')
	SA_p=re.compile(r'SA:Z:([^,]+),([^,]+),[+-],([^,]+),[^\t]+')
	
	out_bam=open(chromosome+"_clips","w")
	out_indel=open(chromosome+"_indel","w")
	out_split=open(chromosome+"_split","w")
	out_break=open(chromosome+"_breakpoint","w")
	out_del=open(chromosome+"_deletion","w")
	out_large_ins=open(chromosome+"_large_insertion","w")
	out_trans=open(chromosome+"_translocation","w")
	out_inv=open(chromosome+"_inversion","w")
	left_del,right_del={},{}
	breakpoint={}
	
	if int(read_length)<190:
		softclip_length=5
	else:
		softclip_length=10
	def asc (seq):
		high=0
		for i in range(len(seq)):
			if ord(seq[i])>=53:
				high+=1
		return str('{:4.3f}'.format(high/len(seq)))
	def merge (attach1,attach2):
		new=[0]*len(attach1)
		for i in range(len(attach1)):
			new[i]=attach1[i]+attach2[i]
		return new
	def cigar_pos(pos,cigar,match_p):
		while True:
			m=match_p.search(cigar)
			if not m: break
			if m.group(2)=="M" or m.group(2)=="D":
				pos=str(int(pos)+int(m.group(1)))
			cigar=cigar[len(m.group(0)):]
		return pos
	
	command= subprocess.Popen(['samtools','view','-h',bam,chromosome], stdout=subprocess.PIPE)

	while True:
		l= command.stdout.readline().decode('utf-8').rstrip()
		if not l: break
		if l[0]=='@':
			out_bam.write(l+'\n')
			continue
		line=l.split('\t')
		MC=MC_p.search(l)
		if MC:
			mc=MC.group(0)
		else:
			mc='NA'
		SA=SA_p.search(l)
		if SA:
			sa=SA.group(0)
		else:
			sa='NA'
		XA=XA_p.search(l)
		if XA:
			xa=XA.group(0)
		else:
			xa='NA'
		mate='0'
		mate_m=re.search(r'[DI]',mc)
		if mate_m:
			mate='1'
		hp='hp1'
		if int(line[1])%2048 >=1024 or int(line[1])%8 >=4 or int(line[4])<10: continue
		if int(line[1])%256 >=128:
			read="R2"
		elif int(line[1])%128 >=64:
			read="R1"
		elif int(line[1])%2 <1:
			continue
		else:
			continue
		barcode='NA'
		cigar=line[5]
		pos= line[3]
		while True:
			m=match_p.search(cigar)
			if not m: break
			if m.group(2)=="I" or m.group(2)=="D":
				indel=indel_p.search(line[5])
				if indel and int(m.group(1))>=1:
					out_indel.write('\t'.join([line[2],pos,str(int(pos)+1),hp,m.group(1)+':'+m.group(2),'\t'.join(line[0:9]),mc,sa])+'\n')
			if m.group(2)=="M" or m.group(2)=="D":
				pos=str(int(pos)+int(m.group(1)))
			cigar=cigar[len(m.group(0)):]
		seq_m=re.search(r'H',line[5])
		if seq_m:
			left_match,left_clip,left_seq,right_match,right_clip,right_seq='-','-','-','-','-','-'
		direction='NA'
		left=left_p.search(line[5])
		if left and int(left.group(3))>=softclip_length:
			direction='left'
			if SA and SA.group(1)==line[2]:
				SA_pos=cigar_pos(SA.group(2),SA.group(3),match_p)
				if int(line[1])%16 <8 and line[6]=='=' and int(pos)<int(SA.group(2)) :
					MC_pos=cigar_pos(line[7],MC.group(1),match_p)
					if not (int(MC_pos)-int(line[3])<int(read_length)-int(min_insert_size)/2 or int(SA_pos)-int(line[7])<int(read_length)-int(min_insert_size)/2):
						continue
			left_len=left.group(1)
			if not seq_m:
				left_seq=line[9][int(left.group(1)):]
				left_match=asc(line[10][0:int(left.group(1))])
				left_clip=asc(line[10][int(left.group(1)):])
				if float(left_match)>=0.6 and float(left_clip)>=0.6:
					out_bam.write(l+'\n')
		right=right_p.search(line[5])
		if right and int(right.group(1))>=softclip_length:
			direction='right'
			if SA and SA.group(1)==line[2]:
				SA_pos=cigar_pos(SA.group(2),SA.group(3),match_p)
				if int(line[1])%16 <8 and line[6]=='=' and int(SA_pos)<int(line[3]) :
					MC_pos=cigar_pos(line[7],MC.group(1),match_p)
					if not (int(MC_pos)-int(SA.group(2))<int(read_length)-int(min_insert_size)/2 or int(pos)-int(line[7])<int(read_length)-int(min_insert_size)/2):
						continue
			right_len=right.group(3)
			if not seq_m:
				right_seq=line[9][0:len(line[9])-int(right.group(3))]
				right_match=asc(line[10][len(line[9])-int(right.group(3)):])
				right_clip=asc(line[10][0:len(line[9])-int(right.group(3))])
				if float(right_match)>=0.6 and float(right_clip)>=0.6:
					out_bam.write(l+'\n')
		if direction=='NA':
			whole=whole_p.search(line[5])
			if whole:
				out_bam.write(l+'\n')
		attach=[0,0,0,0,0,0]
		if direction=='left' or direction=='right':
			attach=merge(attach,[1,0,0,0,0,0])
		if SA or XA:
			attach=merge(attach,[0,1,0,0,0,0])
		if line[6]=='=' and abs(int(line[8]))>=int(max_insert_size):
			attach=merge(attach,[0,0,1,0,0,0])
		if line[6]=='=' and abs(int(line[8]))<=int(min_insert_size) and int(line[1])%16<8:
			attach=merge(attach,[0,0,0,1,0,0])
		if line[6]!='=':
			hs_m = re.search(r'^(hs)|\*',line[6])
			if not hs_m:
				attach=merge(attach,[0,0,0,0,1,0])
			else:
				attach=merge(attach,[0,0,0,0,0,1])
		attach_out='\t'.join(map(str, attach))
		if SA and direction=='left':
			out_split.write('\t'.join([line[2],str(int(line[3])+int(left_len)),str(int(line[3])+int(left_len)+1),hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
		elif SA and direction=='right':
			out_split.write('\t'.join([line[2],str(int(pos)-int(right_len)),str(int(pos)-int(right_len)+1),hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		elif XA and direction=='left':
			out_split.write('\t'.join([line[2],str(int(line[3])+int(left_len)),str(int(line[3])+int(left_len)+1),hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,xa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
		elif XA and direction=='right':
			out_split.write('\t'.join([line[2],str(int(pos)-int(right_len)),str(int(pos)-int(right_len)+1),hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,xa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		#if int(line[1])>=2048 or int(line[1])%512>=256 or int(line[4])<20:
		#	continue
		if direction=='left' and int(left.group(3))>=10 and attach[3]!=1:
			out_break.write('\t'.join([line[2],str(int(line[3])+int(left_len)),str(int(line[3])+int(left_len)+1),hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
		elif direction=='right' and int(right.group(1))>=10 and attach[3]!=1:
			out_break.write('\t'.join([line[2],str(int(pos)-int(right_len)),str(int(pos)-int(right_len)+1),hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		if line[6]=='=' and ((int(line[1])%64>=32 and int(line[1])%32>=16) or (int(line[1])%64<32 and int(line[1])%32<16)) and int(line[1])%16<8:
			if direction=='NA':
				out_inv.write('\t'.join([line[2],pos,line[7],hp,"0:"+direction,'\t'.join(line[0:9]),mc,sa,'NA',mate,attach_out])+'\n')
			elif direction=='left':
				out_inv.write('\t'.join([line[2],str(int(line[3])+int(left_len)),line[7],hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
			elif direction=='right':
				out_inv.write('\t'.join([line[2],str(int(pos)-int(right_len)),line[7],hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		elif line[6]=='=' and abs(int(line[8]))>=int(max_insert_size):
			if direction=='NA':
				out_del.write('\t'.join([line[2],pos,line[7],hp,"0:"+direction,'\t'.join(line[0:9]),mc,sa,'NA',mate,attach_out])+'\n')
			elif int(line[1])%32<16 and direction=='left':
				out_del.write('\t'.join([line[2],str(int(line[3])+int(left_len)),line[7],hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
			elif int(line[1])%32>=16 and direction=='right':
				out_del.write('\t'.join([line[2],str(int(pos)-int(right_len)),line[7],hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		elif line[6]!='=' and (not hs_m):
			if direction=='NA':
				out_trans.write('\t'.join([line[2],pos,line[6]+':'+line[7],hp,"0:"+direction,'\t'.join(line[0:9]),mc,sa,'NA',mate,attach_out])+'\n')
			elif int(line[1])%32<16 and direction=='left':
				out_trans.write('\t'.join([line[2],str(int(line[3])+int(left_len)),line[6]+':'+line[7],hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
			elif int(line[1])%32>=16 and direction=='right':
				out_trans.write('\t'.join([line[2],str(int(pos)-int(right_len)),line[6]+':'+line[7],hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')
		elif (line[6]!='=' and hs_m) or (int(line[1])%16>=8):
			if direction=='NA':
				out_large_ins.write('\t'.join([line[2],pos,line[6]+':'+line[7],hp,"0:"+direction,'\t'.join(line[0:9]),mc,sa,'NA',mate,attach_out])+'\n')
			elif int(line[1])%32<16 and direction=='left':
				out_large_ins.write('\t'.join([line[2],str(int(line[3])+int(left_len)),line[6]+':'+line[7],hp,left_len+':'+direction,'\t'.join(line[0:9]),mc,sa,left_match+":"+left_clip+':'+left_seq,mate,attach_out])+'\n')
			elif int(line[1])%32>=16 and direction=='right':
				out_large_ins.write('\t'.join([line[2],str(int(pos)-int(right_len)),line[6]+':'+line[7],hp,right_len+':'+direction,'\t'.join(line[0:9]),mc,sa,right_match+":"+right_clip+':'+right_seq,mate,attach_out])+'\n')

