# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Create a projected marker (one axis)

Usage:
    python create_projected_marker --input test.c3d --marker "Jugular" --markerVia "Xiphoid" --axis "y" --newMarkerName "J_proj_Xiphoid_Y" --output "newfile.trc"
    or import as module

Requirements:
    btk
    numpy

"""

text="create_projected_marker module"

def create_projected_marker(acq,args):

    import numpy as np
  
    inputFile = args.input
    outputFile = args.output
    marker1 = args.marker
    marker2 = args.markerVia
    coordinateVia = args.axis # this is a projection on x, y or z!
    newMarkerName = args.newMarkerName
    
    # Create an object (point) for each marker
    point1 = acq.GetPoint(marker1)
    point2 = acq.GetPoint(marker2)
    
    # For each frame, get the xyz of point1
    ## point1.GetValues()[0,0] # get the first row, first column (frame 0, x coordinate)
    ## point1.GetValues()[0,1] # get the first row, second column (frame 0, y coordinate)
    ## etc...
    # and save the values of interest to create a new marker

    ## create a 3 columns numpy array
    number_steps = acq.GetLastFrame() - acq.GetFirstFrame() +1
    newpointStructure = (number_steps,3)
    newValue = np.ones(newpointStructure) # identity numpy array with 3 colum and PointFrameNumber rows.
    newValue[:] = np.nan # fill with NaNs to make any mistake obvious
    
    ######################################################
    # Loop
    ######################################################

    i = 0
    while i < number_steps:
        point1_X = point1.GetValues()[i,0]
        point1_Y = point1.GetValues()[i,1]
        point1_Z = point1.GetValues()[i,2]
        
        point2_X = point2.GetValues()[i,0]
        point2_Y = point2.GetValues()[i,1]
        point2_Z = point2.GetValues()[i,2]
      
        if (coordinateVia == "x" or coordinateVia == "X") : 
            newValue[i,0] = point2_X # X value at this step
            newValue[i,1] = point1_Y # Y value at this step
            newValue[i,2] = point1_Z # Z value at this step

        elif (coordinateVia == "y" or coordinateVia == "Y") :
            newValue[i,0] = point1_X # X value at this step
            newValue[i,1] = point2_Y # Y value at this step
            newValue[i,2] = point1_Z # Z value at this step

        elif (coordinateVia == "z" or coordinateVia == "Z") : 
            newValue[i,0] = point1_X # X value at this step
            newValue[i,1] = point1_Y # Y value at this step
            newValue[i,2] = point2_Z # Z value at this step

        else:
            print("Did not recognise the coordinates (has to be 'x', 'y' or 'z').")
            return

        i+=1

    ######################################################
    # Add the array as a new point
    ######################################################
        
    newpoint = btk.btkPoint(number_steps) # create an empty new point object #newpoint = btk.btkPoint(acq.GetPointFrameNumber()) # create an empty new point object
    newpoint.SetLabel(newMarkerName) # set newPoint as label
    newpoint.SetValues(newValue) # set the value
    acq.AppendPoint(newpoint) # append the new point into the acquisition object

    return acq



if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Create midpoint marker', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--input',         '-i',  metavar = 'input',         type = str, help = 'The input file to load (.c3d or .trc)',       required=True)
    parser.add_argument ('--marker',        '-m',  metavar = 'marker1',       type = str, help = 'The name of the marker to project',           required=True)
    parser.add_argument ('--markerVia',     '-mv', metavar = 'marker2',       type = str, help = 'The name of the via marker',                  required=True)
    parser.add_argument ('--axis',          '-a',  metavar = 'marker2',       type = str, help = 'The axis of projection (x,y,z)',              required=True)
    parser.add_argument ('--newMarkerName', '-nm', metavar = 'newMarkerName', type = str, help = 'The name of new marker that will be created', required=True)
    parser.add_argument ('--output',        '-o',  metavar = 'output',        type = str, help = 'The output file to write (.c3d or .trc)',     required=True)
    
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
    # Create the projected marker
    ######################################################
    acq_modified = create_projected_marker(acq,args)

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

