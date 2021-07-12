#!/usr/bin/env python
# coding: utf-8

import sys
import re
import argparse
import numpy as np
import pandas as pd


class retrive_coordinates():
    """
    Return positions for the genomic and query sequences.

    CIGAR: 2M5D2I3M
    hypotethical genomic sequence: MMDDDDDIIMMM

    alignment match (can be a sequence match or mismatch) = 'M'
    deletion from the reference = 'D'
    insertion to the reference = 'I'
    skipped region from the reference = 'N'
    soft clipping (clipped sequences present in SEQ) = 'S'

    Parameters:
    CIGAR - string
    Genomic Start - int
    Transcript/Query Start - int
    """

    def __init__(self, cigar=None, genomic_start=0, transcript_start=0):
        self.cigar = self.__check_cigar(cigar)
        self.genomic_start = self.__check_coordinate(genomic_start)
        self.transcript_start = self.__check_coordinate(transcript_start)
        self.coordinates = self.__get_coordinates(cigar,
                                                  genomic_start,
                                                  transcript_start)

    @staticmethod
    def __check_cigar(cigar=None):
        """A function that run a sanity test on the CIGAR string!"""
        if not isinstance(cigar, str):
            raise TypeError(
                f"CIGAR must be string, not {type(cigar)}"
            )
        cigar_set = set(re.findall(r'[A-Z, a-z]', cigar))
#  print(cigar_set)

        invalid_chars = set()

        for char in cigar_set:
            if (char not in ['M', 'D', 'I', 'S', 'N'] or char.islower()):
                invalid_chars.add(char)

        #  print(invalid_chars)
            if len(invalid_chars) > 0:
                raise ValueError(
                    f"unknown character in CIGAR found: {' '.join(invalid_chars)}"
                )
        return cigar

    @staticmethod
    def __check_coordinate(number=None):
        """
        A function that look for the genomic/transcript/query coordinates
        in input files to make sure they are in the tight type!
        """
        if not isinstance(number, int):
            raise TypeError(
                    f"coordinate must be int, not {type(number)}"
                )
        return number

    @staticmethod
    def __get_coordinates(cigar, genomic_start, transcript_start):
        """A function that translates query posiotions to genomic positions!"""
        cSeq = re.findall(r'[A-Z]', cigar)
        cLen = [int(x) for x in re.findall(r'\d+', cigar)]
        cigar_seq = ''.join(map(str, (e1*e2 for e1, e2 in zip(cLen, cSeq))))

        g_index = []
        gap = 0
        count = genomic_start
        for char in cigar_seq:
            if char not in ['I', 'S']:
                g_index.append(count)
                count += 1
            else:
                g_index.append("G"+str(gap))
                gap += 1
        #  print(g_index)

        t_index = []
        gap = 0
        count = transcript_start
        for char in cigar_seq:
            if char not in ['D', 'N']:
                t_index.append(count)
                count += 1
            else:
                t_index.append("G"+str(gap))
                gap += 1
        t_index = [str(x) for x in t_index]
        # print(t_index)
        coordinates = dict(zip(t_index, g_index))
        return coordinates


def run(args):
    """A function to read input files and build a database of coordinates"""
    genome_coord = pd.read_csv(
        args.reference, sep='\t',
        header=None,
        skip_blank_lines=True,
        names=["c1", "c2", "C3", "c4"])

    transcript_coord = pd.read_csv(
        args.query, sep='\t',
        header=None,
        skip_blank_lines=True,
        names=["c1", "c2"])
    # print(transcript_coord)

    fout = open(args.output, "w")

    database = np.array(transcript_coord.merge(genome_coord, on='c1'))
    # print(database)
    df = pd.DataFrame()
    for i in range(0, len(database)):
        query_coordinate = retrive_coordinates(str(database[i][4]), database[i][3], 0)
        genmic_coordinate = database[: , [0, 1, 2]]
        query_position = str(query_coordinate.coordinates[str(database[i][1])])
        row = pd.DataFrame(np.append(genmic_coordinate[i], \
        					int(query_position)).reshape(-1, 4))
        df = df.append(row)

    fout.write(df.to_string(index=False))
    fout.close()


def main():
    """A function to get the inputs, run the script and write the output"""
    description = "build a database, run algorithm and write the output"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--reference",
        "-r",
        dest="reference",
        help="fasta input file",
        type=str,
        required=True)

    parser.add_argument(
        "--query",
        "-q",
        dest="query",
        help="fasta input file",
        type=str,
        required=True)

    parser.add_argument(
        "--output",
        "-out",
        dest="output",
        help="fastq output filename",
        type=str,
        required=True)

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
