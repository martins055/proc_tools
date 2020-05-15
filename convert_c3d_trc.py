#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    use Btk to read/write c3d and trc files


Usage:
    python convert_c3d_trc.py -i inputFile.c3d/trc -o outputFile.c3d/trc
    or import as module

Requirements:
    btk

"""

text="convert_c3d_trc module"

import btk

def read_c3dtrc(inputFile):
    try:
        reader = btk.btkAcquisitionFileReader() # build a btk reader object
        reader.SetFilename(inputFile) # set a filename to the reader
        reader.Update()
        acq = reader.GetOutput() # acq is the btk aquisition object
    except:
        print("Error loading btk reader (input file probably wrong)")
    return acq

def write_c3dtrc(acq,outputFile):
    try:
        writer = btk.btkAcquisitionFileWriter()
        writer.SetInput(acq)
        writer.SetFilename(outputFile)
        writer.Update()
    except:
        print("Error writting (did you specify an output file?")



if __name__ == "__main__":

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='setOrigin', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument ('--input',  '-i',  metavar = 'input',  type = str, help = 'The input file to load (.c3d or .trc)',   required=True)
    parser.add_argument ('--output', '-o',  metavar = 'output', type = str, help = 'The output file to write (.c3d or .trc)', required=True)
    args = parser.parse_args()

    # Read the input file
    acq = read_c3dtrc(args.input)

    # Save the output file
    write_c3dtrc(acq,args.output)
