#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Takes a marker and defines it as the origin in the motion file.
    Export is either in .trc or .c3d format: provide the extension in the filename

Usage:
    python setOrigin.py -i inputFile.c3d  -m "myOriginMarker" -o outputFile.trc
    or import as module

Requirements:
    btk

"""

text="setOrigin module"

def setOrigin(acq,markerOrigin):

    nombreDeFrames = acq.GetLastFrame() - acq.GetFirstFrame() +1

    # Loop through each frame

    for frameNumber in range(0, nombreDeFrames):

        print ("Processing frame number {}".format(frameNumber))

        # Getting coordinates of our originMarker at this frame
        try:
            originCoordinates = acq.GetPoint(args.markerOrigin).GetValues()[frameNumber,:]
            xValueOrigin = originCoordinates[0]
            yValueOrigin = originCoordinates[1]
            zValueOrigin = originCoordinates[2]
        except: print("Cannot find the markerOrigin {}".format(args.markerOrigin))

        # Loop through all the markers and substract the values of the origin marker
        for pointNumber in range(0, acq.GetPointNumber()):
            x = pointNumber

            print("Processing marker number {} ({}) frame {}: ".format(x , acq.GetPoint(pointNumber).GetLabel(),frameNumber))
            
            # Get value of current point at current frame : acq.GetPoint(pointNumber).GetValues()
            point = acq.GetPoint(x).GetValues()[frameNumber,:]
            xValueCurrent = point[0]
            yValueCurrent = point[1]
            zValueCurrent = point[2]

            # Update values by substracting values of originMarker
            acq.GetPoint(x).SetValue(frameNumber,0,xValueCurrent-xValueOrigin)
            acq.GetPoint(x).SetValue(frameNumber,1,yValueCurrent-yValueOrigin)
            acq.GetPoint(x).SetValue(frameNumber,2,zValueCurrent-zValueOrigin)

            # Making sure it's updated
            #pointUpdated = acq.GetPoint(x).GetValues()[frameNumber,:]
            #print(pointUpdated[:])

    return acq



if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse
    parser = argparse.ArgumentParser(description='setOrigin', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument ('--input',        '-i',  metavar = 'input',        type = str, help = 'The input file to load (.c3d or .trc)',             required=True)
    parser.add_argument ('--markerOrigin', '-m',  metavar = 'markerOrigin', type = str, help = 'The name of the marker that will be set as origin', required=True)
    parser.add_argument ('--output',       '-o',  metavar = 'output',       type = str, help = 'The output file to write (.c3d or .trc)',           required=True)
    args = parser.parse_args()
    
    # If all the arguments have been provided, load the file with btk th#!/usr/bin/env python3en start the function

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
    # Set the origin
    ######################################################
    acq_modified = setOrigin(acq,args.markerOrigin)

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

