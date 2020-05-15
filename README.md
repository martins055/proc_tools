# Tools
Pieces of code that could be useful

Import as modules or use as standalone scripts with python script.py --help

### Read_write_c3d_trc module

**Description:**

    use Btk to read/write c3d and trc files

**Standalone usage:**

    To convert a c3d to trc:
    python convert_c3d_trc.py -i inputFile.c3d/trc -o outputFile.c3d/trc

### setOrigin module

**Description:**

    Takes a marker and defines it as the origin in the motion file.
    Export is either in .trc or .c3d format: provide the extension in the filename

**Standalone usage:**
    
    python setOrigin.py -i inputFile.c3d/trc  -m "myOriginMarker" -o outputFile.c3d/trc

### Create midpoint marker module

**Description:**

    Create a midpoint marker between two existing markers

**Standalone usage:**

    python create_midpoint_marker.py -i inputFile.c3d/trc -o outputFile.c3d/trc -m1 "marker1" -m2 "marker2" -nm "newMarkerName"

### Create projected marker module

**Description:**

    Create a projected marker (one axis)

**Standalone usage:**

    python create_projected_marker --input test.c3d --marker "Jugular" --markerVia "Xiphoid" --axis "x" --newMarkerName "J_proj_Xiphoid_Y" --output "newfile.trc"

### Create anatomical marker module

**Description:**

    Create an anatomical marker based on the location of the a cluster of markers in a motion file

    It requires a calibration file where all marker positions are known

    Example of use: to virtualize position of epicondyles from a humerus cluster

**Standalone usage:**

    python3 create_anatomical_marker.py --calibrationFile "test.c3d/trc" --calibrationFrame 0 --clusterMarkers "HUM_CL-SupAnt","HUM_CL-SupPost","HUM_CL-InfAnt" --anatMarkerName "EPI_MED" --motionFile "test.trc" --newMarkerName "NewMarkerCustomName" --outputFile "myOutputFile.c3d/trc"

### emg-trigno-stream

**Description:**

    Real-time streaming of Delsys EMG in a web browser
    
    This python script connects to the Windows station that has the Trigno connected to, and the "Trigno Control Utility" running. It then uses a websocket to stream the data and is accessible via a web browser (requires a http server)

**Usage:**

    Config values are hard coded. Start the python server (python server.py) and display plot.php in your web browser (requires a http server running)

