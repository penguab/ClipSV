# ClipSV (Structural variation detection with clipped reads)

A software to detect structural variations in human genomes by spliced alignment and local assembly.

Author: Peng Xu

Email: pxu@uabmc.edu

Draft date: June. 4, 2019

## Description

ClipSV was developed to detect structural variations by spliced alignment and local assembly. It primarily depends on clipped reads from short-read (optimal 250bp) sequencing platform. ClipSV was optimized to discover INDELS (2bp-50bp) and structural variations (>=50bp) in germline human genomes.

## System requirements and dependency

The program was tested on a x86_64 Linux system with 12 cores, each with a 4GB physical memory. The work can be usually finished within 6 hours per 30x whole genome sequencing sample.

Dependency: Python3, samtools, minimap2, bedtools, velvet should be installed in current path.


## Installation

```
git clone https://github.com/penguab/ClipSV.git
```
Then, please also add this directory to your PATH:
```
export PATH=$PWD/ClipSV/:$PATH
```

## Usage

ClipSV needs two files as inputs. The first is a bam file from whole genome sequencing. The second is the genome reference indexed by minimap2 (To generate index file, use command "minimap2 -d genome.mmi genome.fa").
```
python clipsv.py -b <bam file> -g <genome.mmi>
```


## News

6/4/2019: First version released.

