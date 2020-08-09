#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Rename a list of markers in a c3d or trc file

Usage:
    python3 rename_markers.py --inputFile "test.trc" --from "M1original","M2original" --to "M1modified","M2modified" --outputFile test_renamed.trc
    or import as module

Requirements:
    btk

Ressources:
	https://pycgm2.github.io/resources/cheat%20sheet%20BTK0.3.pdf

"""

def rename_markers(acq,args):

	# Load the marker names
	markerListFrom = args.makerListFrom.split(",") # create a list out of the string with ","
	markerListTo = args.makerListTo.split(",")

	# Check that we have same number of labels
	if (len(markerListFrom) != len(markerListTo)):
		print("Markers From and markers To do not have the same size. Exitting.")
		quit()

	# Rename from one list to another
	for x in range(len(markerListFrom)): 
		print("[{}] Renaming: From {} to {}".format(x,markerListFrom[x],markerListTo[x]))

		point = acq.GetPoint(markerListFrom[x])
		point.SetLabel(markerListTo[x]) # set the new label

	return acq

if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Rename markers', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--inputFile',     '-i', metavar = 'inputFile',      type = str,  help = 'The input file to load (.c3d or .trc)',   required=True)
    parser.add_argument ('--from', '-f',     metavar = 'markerListFrom', type = str,  help = 'List of names of the markers to rename',  required=True)
    parser.add_argument ('--to',   '-t',     metavar = 'markerListTo',   type = str,  help = 'List of the new names of the markers',    required=True)
    parser.add_argument ('--outputFile',    '-o',     metavar = 'outputFile',     type = str,  help = 'The output file to write (.c3d or .trc)', required=True)

    args = parser.parse_args()

    # If all the arguments have been provided, load the files with btk then start the function


    ######################################################
    # Load the input file
    ######################################################
    import sys
    import btk
    try:
        print("Loading the file file {}".format(args.inputFile))
        reader = btk.btkAcquisitionFileReader() # build a btk reader object
        reader.SetFilename(args.inputFile) # set a filename to the reader
        reader.Update()
        acq = reader.GetOutput() # acq is the btk aquisition object
    except:
        sys.exit("Error reading the input file, exiting")

    ######################################################
    # Rename the markers
    ######################################################
    acq_modified = rename_markers(acq,args)

    ######################################################
    # Save the file
    ######################################################
    print("Saving the file as {}".format(args.outputFile))
    try:
        writer = btk.btkAcquisitionFileWriter()
        writer.SetInput(acq_modified)
        writer.SetFilename(args.outputFile)
        writer.Update()
    except:
        print("Error saving the file")
