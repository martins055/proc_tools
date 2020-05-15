#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Create an anatomical marker based on the location of the a cluster of markers. in a motion file
    It requires a calibration file where all marker positions are known
    Example of use: to virtualize position of epicondyles from a humerus cluster

Usage:
    python3 create_anatomical_marker.py --calibrationFile "test.trc" --calibrationFrame 0 --clusterMarkers "HUM_CL-SupAnt","HUM_CL-SupPost","HUM_CL-InfAnt" --anatMarkerName "EPI_MED" --motionFile "test.trc" --newMarkerName "NewMarkerCustomName" --outputFile "myOutputFile.trc"
    or import as module

Requirements:
    btk
    numpy

To do:
    [] in the calibration file, calculate the average of the positions instead of just one frame
    [] allow to define 4 or more markers instead of 3 for the cluster
    [] optimize for real time processing

"""

text="create_anatomical_marker module"

def create_anatomical_marker(acqCalibration,acqMotion,args):

    import numpy as np

    # Tidying up some variables
    calibrationFrame = args.calibrationFrame
    clusterMarkersNamesList = args.clusterMarkers.split(",") # create a list out of the clusterMarkerNames string

    def rigid_transform_3D(A, B):
    
        # "Least-Squares Fitting of Two 3-D Point Sets", Arun, K. S. and Huang, T. S. and Blostein, S. D, IEEE Transactions on Pattern Analysis and Machine Intelligence, Volume 9 Issue 5, May 1987
        # "A Method for Registration of 3-D Shapes" by Besl and McKay, 1992.
        # https://github.com/nghiaho12/rigid_transform_3D/

        assert len(A) == len(B)

        num_rows, num_cols = A.shape;

        if num_rows != 3:
            raise Exception("matrix A is not 3xN, it is {}x{}".format(num_rows, num_cols))

        [num_rows, num_cols] = B.shape;
        if num_rows != 3:
            raise Exception("matrix B is not 3xN, it is {}x{}".format(num_rows, num_cols))

        # find mean column wise
        centroid_A = np.mean(A, axis=1)
        centroid_B = np.mean(B, axis=1)

        # subtract mean
        Am = A - np.tile(centroid_A, (1, num_cols))
        Bm = B - np.tile(centroid_B, (1, num_cols))

        # dot is matrix multiplication for array
        H = Am * np.transpose(Bm)

        # find rotation
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T * U.T

        # special reflection case
        if np.linalg.det(R) < 0:
            #print("det(R) < R, reflection detected!, correcting for it ...\n");
            Vt[2,:] *= -1
            R = Vt.T * U.T

        t = -R*centroid_A + centroid_B

        return R, t

    ##############################################################################
    # Get cluster and anatomical markers coordinates from the calibration file
    ##############################################################################

    # Get cluster markers

    # Create an object (point) for each marker
    point1 = acqCalibration.GetPoint(clusterMarkersNamesList[0])
    point2 = acqCalibration.GetPoint(clusterMarkersNamesList[1])
    point3 = acqCalibration.GetPoint(clusterMarkersNamesList[2])

    point1x = point1.GetValues()[calibrationFrame,0]
    point1y = point1.GetValues()[calibrationFrame,1]
    point1z = point1.GetValues()[calibrationFrame,2]
    point2x = point2.GetValues()[calibrationFrame,0]
    point2y = point2.GetValues()[calibrationFrame,1]
    point2z = point2.GetValues()[calibrationFrame,2]
    point3x = point3.GetValues()[calibrationFrame,0]
    point3y = point3.GetValues()[calibrationFrame,1]
    point3z = point3.GetValues()[calibrationFrame,2]

    cluster1 = np.mat([
                            [ point1x , point1y , point1z ],
                            [ point2x , point2y , point2z ],
                            [ point3x , point3y , point3z ]
                            ])

    # Get anatomical marker

    pointAnat1 = acqCalibration.GetPoint(args.anatMarkerName)

    pointAnat1x = pointAnat1.GetValues()[calibrationFrame,0]
    pointAnat1y = pointAnat1.GetValues()[calibrationFrame,1]
    pointAnat1z = pointAnat1.GetValues()[calibrationFrame,2]

    ############################################################################################################################
    # Go through the motion file, calculate rotation and translation matrices and calculate new anatomical marker coordinates
    ############################################################################################################################

    ## create a 3 columns numpy array that will later become our new point in btk
    number_steps = acqMotion.GetPointFrameNumber() # give the number of frames
    newpointStructure = (number_steps,3)
    newValue = np.ones(newpointStructure) # identity numpy array with 3 colum and PointFrameNumber rows.
    newValue[:] = np.nan # fill with NaNs to make any mistake obvious

    i=0
    for frame in range(0, number_steps ): # for each frame of the motion file

        # Get the cluster2 from the motion file at this specific frame

        point1x = point1.GetValues()[frame,0]
        point1y = point1.GetValues()[frame,1]
        point1z = point1.GetValues()[frame,2]
        point2x = point2.GetValues()[frame,0]
        point2y = point2.GetValues()[frame,1]
        point2z = point2.GetValues()[frame,2]
        point3x = point3.GetValues()[frame,0]
        point3y = point3.GetValues()[frame,1]
        point3z = point3.GetValues()[frame,2]

        cluster2 = np.mat([
                                [ point1x , point1y , point1z ],
                                [ point2x , point2y , point2z ],
                                [ point3x , point3y , point3z ]
                                ])

        # Calculate rotation and translation matrices between the two clusters (cluster from calibration file, and cluster from this motion frame)
        anat1 = np.mat([ pointAnat1x , pointAnat1y , pointAnat1z ])
        anat1t = anat1.transpose()
        cluster1t = cluster1.transpose()
        cluster2t = cluster2.transpose()

        ret_R, ret_t = rigid_transform_3D(cluster1t, cluster2t)

        # Recover coordinates of the anatomical marker at this frame of the motion file, from the calibration file
        test_anat = (ret_R*anat1t) + ret_t
        test_anat_norot = anat1t + ret_t
        #print("frame {}, test anat recovered is: {}".format(i,test_anat))
        #print("x = {}, y = {}, z={}".format(test_anat[0],test_anat[1],test_anat[2]))

        # Add the values to a numpy array, we will append it to the aquisition once we have all the values (after this loop)
        newValue[i,0] = test_anat[0] # X value at this step
        newValue[i,1] = test_anat[1] # Y value at this step
        newValue[i,2] = test_anat[2] # Z value at this step

        i+=1

    ######################################################
    # Add the array as a new point
    ######################################################

    newpoint = btk.btkPoint(number_steps) # create an empty new point object
    newpoint.SetLabel(args.newMarkerName) # set newPoint as label
    newpoint.SetValues(newValue) # set the value
    acqMotion.AppendPoint(newpoint) # append the new point into the acquisition object

    return acqMotion



if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Create anatmical marker', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--calibrationFile',  '-cfile',    metavar = 'calibrationFile',  type = str,  help = 'The calibration file to load (.c3d or .trc)',   required=True)
    parser.add_argument ('--calibrationFrame', '-cframe',   metavar = 'calibrationFrame', type = int,  help = 'The frame of the calibration file to consider', required=True)
    parser.add_argument ('--clusterMarkers',   '-cmarkers', metavar = 'clusterMarkers',   type = str,  help = 'List of names of the 3 cluster markers',        required=True)
    parser.add_argument ('--anatMarkerName',   '-amarker',  metavar = 'anatMarkerName',   type = str,  help = 'The name of anatomical marker to consider',     required=True)
    parser.add_argument ('--motionFile',       '-mfile',    metavar = 'motionFile',       type = str,  help = 'The motion file to load',                       required=True)
    parser.add_argument ('--newMarkerName',    '-nmarker',  metavar = 'newMarkerName',    type = str,  help = 'The name of new marker that will be created',   required=True)
    parser.add_argument ('--outputFile',       '-o',        metavar = 'outputFile',       type = str,  help = 'The output file to write (.c3d or .trc)',       required=True)

    args = parser.parse_args()

    # If all the arguments have been provided, load the files with btk then start the function

    ######################################################
    # Load the files
    ######################################################
    import sys
    import btk
    try:
        print("Loading the calibration file {}".format(args.calibrationFile))
        readerCalibration = btk.btkAcquisitionFileReader() # build a btk reader object
        readerCalibration.SetFilename(args.calibrationFile) # set a filename to the reader
        readerCalibration.Update()

        print("Loading the motion file {}".format(args.motionFile))
        acqCalibration = readerCalibration.GetOutput() # acq is the btk aquisition object
        readerMotion = btk.btkAcquisitionFileReader() # build a btk reader object
        readerMotion.SetFilename(args.motionFile) # set a filename to the reader
        readerMotion.Update()
        acqMotion = readerMotion.GetOutput() # acq is the btk aquisition object
    except:
        sys.exit("Error reading one of the files, exiting")

    ######################################################
    # Create the anatomical marker
    ######################################################
    acq_modified = create_anatomical_marker(acqCalibration,acqMotion,args)

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
