#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Martin

Description:
    Create an anatomical marker based on the location of the a cluster of markers in a motion file
    It requires a calibration file where all marker positions are known
    Example of use: to virtualize position of epicondyles from a humerus cluster

Usage:
    python3 create_anatomical_marker.py --calibrationFile "test.trc" --calibrationFrame 0 --clusterMarkers "HUM_CL-SupAnt","HUM_CL-SupPost","HUM_CL-InfAnt" --anatMarkerName "EPI_MED" --motionFile "test.trc" --newMarkerName "NewMarkerCustomName" --outputFile "myOutputFile.trc"
    # can specify --onlyMissingFrames to keep existing frames if only some parts are missing and need reconstructing
    or import as module

Requirements:
    btk
    numpy

To do:
    [] in the calibration file, calculate the average of the positions instead of just one frame
    [] allow to define 4 or more markers instead of 3 for the cluster (*args/**kwargs)
    [] optimize for real time processing

"""

text="create_anatomical_marker module"

def create_anatomical_marker(acqCalibration,acqMotion,args):

    import numpy as np

    # Tidying up some variables
    calibrationFrame = args.calibrationFrame
    clusterMarkersNamesList = args.clusterMarkers.split(",") # create a list out of the clusterMarkerNames string
    
    print("\nCluster markers name list is {}".format(clusterMarkersNamesList))
    print("Anatomical marker name is {}\n".format(args.anatMarkerName))


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
    point1Calibration = acqCalibration.GetPoint(clusterMarkersNamesList[0])
    point2Calibration = acqCalibration.GetPoint(clusterMarkersNamesList[1])
    point3Calibration = acqCalibration.GetPoint(clusterMarkersNamesList[2])

    point1xCalibration = point1Calibration.GetValues()[calibrationFrame,0]
    point1yCalibration = point1Calibration.GetValues()[calibrationFrame,1]
    point1zCalibration = point1Calibration.GetValues()[calibrationFrame,2]
    point2xCalibration = point2Calibration.GetValues()[calibrationFrame,0]
    point2yCalibration = point2Calibration.GetValues()[calibrationFrame,1]
    point2zCalibration = point2Calibration.GetValues()[calibrationFrame,2]
    point3xCalibration = point3Calibration.GetValues()[calibrationFrame,0]
    point3yCalibration = point3Calibration.GetValues()[calibrationFrame,1]
    point3zCalibration = point3Calibration.GetValues()[calibrationFrame,2]

    cluster1 = np.mat([
                            [ point1xCalibration , point1yCalibration , point1zCalibration ],
                            [ point2xCalibration , point2yCalibration , point2zCalibration ],
                            [ point3xCalibration , point3yCalibration , point3zCalibration ]
                            ])

    print("Cluster 1 is:\n{}\n".format(cluster1))

    # Get anatomical marker

    pointAnat1 = acqCalibration.GetPoint(args.anatMarkerName)

    pointAnat1x = pointAnat1.GetValues()[calibrationFrame,0]
    pointAnat1y = pointAnat1.GetValues()[calibrationFrame,1]
    pointAnat1z = pointAnat1.GetValues()[calibrationFrame,2]

    ############################################################################################################################
    # Go through the motion file, calculate rotation and translation matrices and calculate new anatomical marker coordinates
    ############################################################################################################################

    ## create a 3 columns numpy array that will later become our new point in btk
    #number_steps = acqMotion.GetPointFrameNumber() # give the number of frames
    number_steps = acqMotion.GetLastFrame() - acqMotion.GetFirstFrame() +1 # number_steps = acq.GetPointFrameNumber() # give the number of frames

    newpointStructure = (number_steps,3)
    newValue = np.ones(newpointStructure) # identity numpy array with 3 colum and PointFrameNumber rows.
    newValue[:] = np.nan # fill with NaNs to make any mistake obvious

    # Create an object (point) for each marker
    point1Motion = acqMotion.GetPoint(clusterMarkersNamesList[0])
    point2Motion = acqMotion.GetPoint(clusterMarkersNamesList[1])
    point3Motion = acqMotion.GetPoint(clusterMarkersNamesList[2])
    pointAnatMotion = acqMotion.GetPoint(args.anatMarkerName)

    i=0
    for frame in range(0, number_steps ): # for each frame of the motion file
        print("Motion file, doing frame {}".format(frame))

        # Get the cluster2 from the motion file at this specific frame
        point1xMotion = point1Motion.GetValues()[frame,0]
        point1yMotion = point1Motion.GetValues()[frame,1]
        point1zMotion = point1Motion.GetValues()[frame,2]
        point2xMotion = point2Motion.GetValues()[frame,0]
        point2yMotion = point2Motion.GetValues()[frame,1]
        point2zMotion = point2Motion.GetValues()[frame,2]
        point3xMotion = point3Motion.GetValues()[frame,0]
        point3yMotion = point3Motion.GetValues()[frame,1]
        point3zMotion = point3Motion.GetValues()[frame,2]

        cluster2 = np.mat([
                                [ point1xMotion , point1yMotion , point1zMotion ],
                                [ point2xMotion , point2yMotion , point2zMotion ],
                                [ point3xMotion , point3yMotion , point3zMotion ]
                                ])

        print("Cluster 2 is:\n{}\n".format(cluster2))

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

        ## If we only asked to reconstruct only the missing frames (--onlyMissingFrames),
        ## check if all xyz values exist. If yes copy them, if no reconstruct

        # did we ask to reconstruct only the missing frames?
        print("did we specify missing frames only?")
        # print(args.onlyMissingFrames)
        copyInsteadOfReconstructing = False
        if (args.onlyMissingFrames == True):
            print("YES")
            print("Do we have xyz values for the anatomical marker ({}) at this frame of the motion file?".format(args.anatMarkerName))
            anatxMotion = pointAnatMotion.GetValues()[frame,0]
            anatyMotion = pointAnatMotion.GetValues()[frame,1]
            anatzMotion = pointAnatMotion.GetValues()[frame,2]
            if ( anatxMotion and anatyMotion and anatzMotion != "0.0"):
                print("YES: need to copy, do not reconstruct")
                print("{} ; {} ; {}".format(anatxMotion,anatyMotion,anatzMotion))
                copyInsteadOfReconstructing = True
            else:
                print("NO (at least one missing value) reconstruct, do not copy")
                print("{} ; {} ; {}".format(anatxMotion,anatyMotion,anatzMotion))
            # yes: copy them and skip the cluster part
            # no: reconstruct them            

        if (args.onlyMissingFrames == False):
            print("NO")
            print("We asked to reconstruct all the frames regardless of if some already exist. Do nothing")
            # just go ahead then
        #input()

        # Add the values to a numpy array, we will append it to the aquisition once we have all the values (after this loop)
        if (copyInsteadOfReconstructing == True):
            print("we are copying the values from the original file because the values already exist")
            print("{} ; {} ; {}\n".format(anatxMotion,anatyMotion,anatzMotion))
            newValue[i,0] = anatxMotion # X value at this step
            newValue[i,1] = anatyMotion # Y value at this step
            newValue[i,2] = anatzMotion # Z value at this step
        elif (copyInsteadOfReconstructing == False):
            print("we are generating the values from the original file because the values do NOT already exist")
            print("{} ; {} ; {}\n".format(test_anat[0],test_anat[1],test_anat[2]))
            newValue[i,0] = test_anat[0] # X value at this step
            newValue[i,1] = test_anat[1] # Y value at this step
            newValue[i,2] = test_anat[2] # Z value at this step

        i+=1

    ######################################################
    # Add the array as a new point
    ######################################################

    print("\n\nDEBUG\n\n")
    np.set_printoptions(threshold=sys.maxsize)
    print(np.array_str(newValue, precision=5, suppress_small=False))

    newpoint = btk.btkPoint(number_steps) # create an empty new point object
    newpoint.SetLabel(args.newMarkerName) # set newPoint as label
    newpoint.SetValues(newValue) # set the value
    acqMotion.AppendPoint(newpoint) # append the new point into the acquisition object

    return acqMotion



if __name__ == '__main__':

    # If loaded as main, initialise the parser (to start the program with arguments)
    import argparse

    parser = argparse.ArgumentParser(description='Create anatmical marker', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument ('--calibrationFile',   '-cfile',    metavar = 'calibrationFile',   type = str,  help = 'The calibration file to load (.c3d or .trc)',   required=True)
    parser.add_argument ('--calibrationFrame',  '-cframe',   metavar = 'calibrationFrame',  type = int,  help = 'The frame of the calibration file to consider', required=True)
    parser.add_argument ('--clusterMarkers',    '-cmarkers', metavar = 'clusterMarkers',    type = str,  help = 'List of names of the 3 cluster markers',        required=True)
    parser.add_argument ('--anatMarkerName',    '-amarker',  metavar = 'anatMarkerName',    type = str,  help = 'The name of anatomical marker to consider',     required=True)
    parser.add_argument ('--motionFile',        '-mfile',    metavar = 'motionFile',        type = str,  help = 'The motion file to load',                       required=True)
    parser.add_argument ('--newMarkerName',     '-nmarker',  metavar = 'newMarkerName',     type = str,  help = 'The name of new marker that will be created',   required=True)
    parser.add_argument ('--outputFile',        '-o',        metavar = 'outputFile',        type = str,  help = 'The output file to write (.c3d or .trc)',       required=True)
    parser.add_argument ('--onlyMissingFrames', '-mframes',                                              help = 'Reconstruct on missing frames only',            required=False, action='store_true', default=False)

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
        acqCalibration = readerCalibration.GetOutput() # acq is the btk aquisition object

        print("Loading the motion file {}".format(args.motionFile))
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
