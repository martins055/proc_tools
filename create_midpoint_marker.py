#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Create a midpoint marker between two existing markers

Usage:
    python create_midpoint_marker.py -i inputFile.c3d/trc -o outputFile.c3d/trc -m1 "marker1" -m2 "marker2" -nm "newMarkerName"
    or import as module

Requirements:
    btk
    numpy

"""

text="create_midpoint_marker module"

def create_midpoint_marker(acq,args):
    
    import numpy as np

    # Create an object (point) for each marker
    point1 = acq.GetPoint(args.marker1)
    point2 = acq.GetPoint(args.marker2)

    ######################################################
    # Loop
    ######################################################

    # For each frame, get the xyz of point1
    ## point1.GetValues()[0,0] # get the first row, first column (frame 0, x coordinate)
    ## point1.GetValues()[0,1] # get the first row, second column (frame 0, y coordinate)
    ## etc...
    # and save the values of interest to create a new marker

    ## create a 3 columns numpy array
    try:       
        number_steps = acq.GetLastFrame() - acq.GetFirstFrame() +1
        newpointStructure = (number_steps,3)
        newValue = np.ones(newpointStructure) # identity numpy array with 3 colum and PointFrameNumber rows.
        newValue[:] = np.nan # fill with NaNs to make any mistake obvious
    except:
        print("Could not create empty array")

    i = 0
    while i < number_steps:
        point1_X = point1.GetValues()[i,0]
        point1_Y = point1.GetValues()[i,1]
        point1_Z = point1.GetValues()[i,2]
        
        point2_X = point2.GetValues()[i,0]
        point2_Y = point2.GetValues()[i,1]
        point2_Z = point2.GetValues()[i,2]
        # Add the values to a numpy array, we will append it to the aquisition once we have all the values (after this loop)
        newValue[i,0] = (float(point1_X) + float(point2_X)) / 2.0 # X value at this step
        newValue[i,1] = (float(point1_Y) + float(point2_Y)) / 2.0 # Y value at this step
        newValue[i,2] = (float(point1_Z) + float(point2_Z)) / 2.0 # Z value at this step

        i+=1
   
    ######################################################
    # Add the array as a new point
    ######################################################
    
    newpoint = btk.btkPoint(number_steps) # create an empty new point object
    newpoint.SetLabel(args.newMarkerName) # set newPoint as label
    newpoint.SetValues(newValue) # set the value
    acq.AppendPoint(newpoint) # append the new point into the acquisition object
    
    return acq



if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Create midpoint marker', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--input',         '-i',   metavar = 'input',         type = str, help = 'The input file to load (.c3d or .trc)',       required=True)
    parser.add_argument ('--marker1',       '-m1',  metavar = 'marker1',       type = str, help = 'The name of the 1st marker',                  required=True)
    parser.add_argument ('--marker2',       '-m2',  metavar = 'marker2',       type = str, help = 'The name of the 2nd marker',                  required=True)
    parser.add_argument ('--newMarkerName', '-nm',  metavar = 'newMarkerName', type = str, help = 'The name of new marker that will be created', required=True)
    parser.add_argument ('--output',        '-o',   metavar = 'output',        type = str, help = 'The output file to write (.c3d or .trc)',     required=True)
    
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
    acq_modified = create_midpoint_marker(acq,args)

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

