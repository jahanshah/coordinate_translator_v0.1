<img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/logo2.png" width="120" height="120">

# coordinate_translator 
![](https://img.shields.io/github/languages/count/jahanshah/coordinate_translator_v0.1) 
![](https://img.shields.io/github/languages/top/jahanshah/coordinate_translator_v0.1) 
![](https://img.shields.io/scrutinizer/quality/g/jahanshah/coordinate_translator_v0.1/main) 
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/jahanshah/coordinate_translator_v0.1/main) 
![GitHub Release Date](https://img.shields.io/github/release-date/jahanshah/coordinate_translator_v0.1)


## Summary
`coordinate_translator` is a tool that converts 0-based transcript coordinates to 0-based genomic coordinates using position and CIGAR strings from the input files. The strength of this code is in its performance tuning, by using list comprehensions where possible, use of ‘NumPy’ arrays, use of built-in functions, avoid unnecessary looping, as well as using generators and decorators. Errors are handled based on input specifications; however a more extensive case handling could be performed in future versions.  


## Python dependencies
coordinate_translator requires:
* [Python](https://www.python.org) &gt;= 3.9.6
* [NumPy](http://www.numpy.org) &gt;= 1.21.0
* [Pandas](https://pandas.pydata.org) &gt;= 1.3.0

##  Usage
    
    Takes two input files, with one being the reference file and the other one the query file.
    
    $ coordinates_translator
    usage: coordinates_translator [-h] -f <reference_coordinates.txt> -q <query_coordinates.txt> -out <output.txt>

    Arguments:
      -h,--help                show this help message and exit
      -r,--reference FILE      A four column reference file
      -q,--query FILE          A two column query file
      -out,--output FILE       Output file  
       
    The output is a simple tab-seperated file with four columns: query name, 0-based quary start coordinate, chromosome name, and chromosome coordinates.

## Input File Format
    
   `coordinate_translator` takes two input file:
   1. A four column (tab-separated) file containing the queries. The first column is the query name, and the remaining three columns indicate it’s genomic mapping: chromosome name, 0-based starting position on the chromosome, and CIGAR string indicating the mapping.  
   2. A two column (tab-separated) file indicating a set of queries. The first column is a quary name, and the second column is a 0-based coordinate.  


## Example
  
For example, consider the simple transcript TR1, which aligns to the genome as follows:

                    0    5    10   15   20     25   30   35   40   45   50
      GENOME:CHR1   ACTGTCATGTACGTTTAGCTAGCC--TAGCTAGGGACCTAGATAATTTAGCTAG
       TR1             GTCATGTA-------CTAGCCGGTA-----------AGATAAT 
                       0    5           10   15              20  24 

For This alignment is compactly expressed in the same way as a read alignment in the SAM/BAM format: using a position and **CIGAR** string. In this case, the (0-based) position is CHR1:3, and the **CIGAR** string is `8M7D6M2I2M11D7M`. coordinate_translator assumes that the transcript is always mapped from genomic 5’ to 3’.


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

## Performance:
Given the uncertainty in run time due to computing resources, cache behaviors, etc., the “coordinate_translator.py” code was profiled 
using ‘timeit’. Because ‘timeit’ runs the code many times, at multiple trial, I think it will give a good overall view of code performance. Accordingly, ‘timeit’ was run 1M times to provide a total runtime at the end of the code. This process was repeated 1000 times. The following scatterplot shows the total time distribution across the repeated runs.

<img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/scatter_plot_timeit.png" width="380" height="280">

One limitation here is the lack of comparative assessment of the code due to the absence of an alternative method to compare against,
in terms of time and memory usage. However, I show that the run time remains short and stable across repeated testing. I also acknowledge 
that ‘timeit’ is more suitable for code snippet. Given the ‘length’ of our code ‘timeit’ provides an overall view of code performance. 

To evaluate the complexity of this code, a deterministic profiling was also performed using python's ‘cProfile’ module. 
The performance results are visualized using a python library named ‘snakeviz’. In the Icicle plot below, the root function is the
top most rectangle with functions it calls below it. The amount of time spent inside a function is represented by the width of the rectangle. A rectangle that stretches across the plot represents a function that is taking up most of the time of its calling function. 


<img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/snakeviz_cProfile.png" width="320" height="135">  |  <img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/snakeviz_cProfile_top10.png" width="320" height="135">

Code complexity was assessed by testing a large number of inputs data against time taken to run the code. The results show a linear relationship between the two. 


<img src="https://github.com/jahanshah/coordinate_translator_v0.1/blob/main/images/Complexity_plot.png" width="380" height="280"> 


Code quality was further tested using 'Scrutinizer' that rates different elements of the code including classes, methods, and functions. Combining different metrics such as complexity, coupling and cohesion a score pf 9.35 
is given to the 'coordinate_translater.py' code.



##  Author
Jahanshah Ashkani

##  Citation
    
