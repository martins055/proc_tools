#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Removes a marker. Useful when the value is set to 0, or the list is empty.

Usage:
    python remove_marker.py -i inputFile.c3d/trc -o outputFile.c3d/trc -m1 "markerToDelete"
    or import as module

Requirements:
    btk

Material:
    https://biomechanical-toolkit.github.io/docs/Wrapping/Python/classbtk_1_1btk_acquisition.html#af36d369f3d923ffe33be5fa7e0b12d7f

"""

text="remove_marker module"

def remove_marker(acq,args):

    # Create an object (point)
    point1 = acq.GetPoint(args.marker)

    # need to find the number (in the list) of the choosen marker (can't get the RemovePoint to work otherwise)
    numberOfPoints = acq.GetPointNumber()
    #print("There are {} markers in the file".format(numberOfPoints))
    i = 0
    while i < numberOfPoints: # loop through them and display the labels
        currentName = acq.GetPoint(i).GetLabel()
        #print(i , currentName)
        if (currentName == args.marker):
            #print("Found our marker's number")
            break
        i+=1

    ######################################################
    # Remove the marker
    ######################################################

    #try:
    acq.RemovePoint(i)
    #except:
    #    print("Error removing the point")

    return acq

if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Create midpoint marker', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--input',  '-i',  metavar = 'input',  type = str, help = 'The input file to load (.c3d or .trc)',   required=True)
    parser.add_argument ('--marker', '-m1', metavar = 'marker', type = str, help = 'The name of the marker to delete',        required=True)
    parser.add_argument ('--output', '-o',  metavar = 'output', type = str, help = 'The output file to write (.c3d or .trc)', required=True)
    
    args = parser.parse_args()

    # If all the arguments have been provided, load the file with btk then start the function

    ######################################################
    # Load the file
    ######################################################
    import sys
    import btk
    print("Loading the file {}".format(args.input))
    try:
        reader = btk.btkAcquisitionFileReader() # build a btk reader object
        reader.SetFilename(args.input) # set a filename to the reader
        reader.Update()
        acq = reader.GetOutput() # acq is the btk aquisition object
    except:
        sys.exit("Error reading the file, exiting")

    ######################################################
    # Create the midpoint marker
    ######################################################
    acq_modified = remove_marker(acq,args)

    ######################################################
    # Save the file
    ######################################################
    print("Saving the file as {}".format(args.output))
    try:
        writer = btk.btkAcquisitionFileWriter()
        writer.SetInput(acq_modified)
        writer.SetFilename(args.output)
        writer.Update()
    except:
        print("Error saving the file")

