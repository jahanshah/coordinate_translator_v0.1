<img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/logo2.png" width="120" height="120">

# coordinate_translator 
![](https://img.shields.io/github/languages/top/jahanshah/coordinate_translator_v0.1) 
![](https://img.shields.io/scrutinizer/quality/g/jahanshah/coordinate_translator_v0.1/main) 
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/jahanshah/coordinate_translator_v0.1/main) 
![GitHub Release Date](https://img.shields.io/github/release-date/jahanshah/coordinate_translator_v0.1)


## Summary
`coordinate_translator` is a tool that converts 0-based transcript coordinates to 0-based genomic coordinates using position and CIGAR strings from the input files. The key strength of this tool is .....efficiency... computational feasibility? limitations... 


## Python dependencies
coordinate_translator requires:
* [Python](https://www.python.org) &gt;= 3.9.6
* [NumPy](http://www.numpy.org) &gt;= 1.21.0
* [Pandas](https://pandas.pydata.org) &gt;= 1.3.0

##  Usage
    
    Takes two input files, with one being the transcript reference file and the other one the query file.
    
    $ Coordinates_translator
    usage: Coordinates_translator [-h] -f <reference.txt> -q <transcript_query.txt> -out <output.txt>

    Arguments:
      -h,--help                show this help message and exit
      -r,--reference FILE      A four column reference file
      -q,--query FILE          A two column query file
      -out,--output FILE       Output file  
       
    The output is a simple tab-seperated file with four columns: transcript name, 0-based transcript coordinate, chromosome name, and chromosome coordinates.

## Input File Format
    
   `Coordinate_translator` takes two input file:
   1. A four column (tab-separated) file containing the transcripts. The first column is the transcript name, and the remaining three columns indicate it’s genomic mapping: chromosome name, 0-based starting position on the chromosome, and CIGAR string indicating the mapping.  
   2. A two column (tab-separated) file indicating a set of queries. The first column is a transcript name, and the second column is a 0-based transcript coordinate.  


## Example
  
For example, consider the simple transcript TR1, which aligns to the genome as follows:

                    0    5    10   15   20     25   30   35   40   45   50
      GENOME:CHR1   ACTGTCATGTACGTTTAGCTAGCC--TAGCTAGGGACCTAGATAATTTAGCTAG
       TR1             GTCATGTA-------CTAGCCGGTA-----------AGATAAT 
                       0    5           10   15              20  24 

For This alignment is compactly expressed in the same way as a read alignment in the SAM/BAM format: using a position and **CIGAR** string. In this case, the (0-based) position is CHR1:3, and the **CIGAR** string is `8M7D6M2I2M11D7M`. Coordinate_translator assumes that the transcript is always mapped from genomic 5’ to 3’.


**Input file 1** (reference file):

    TR1   CHR1  3     8M7D6M2I2M11D7M
    TR2   CHR2  10    20M 66M
    
    
**Input file 2** (reference file):  
   
    TR1   4 
    TR2   0
    TR1   13
    TR2   10
    
**Output file:**
    
    TR1   4     CHR1   7 
    TR2   0     CHR2   10
    TR1   13    CHR1   23
    TR2   10    CHR2   20

##  Author
Jahanshah Ashkani

##  Citation
    
