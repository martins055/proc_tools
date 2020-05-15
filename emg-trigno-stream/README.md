# emg-trigno-stream

Real-time streaming of Delsys EMG in a web browser
This python script connects to the Windows station that has the Trigno connected to, and the "Trigno Control Utility" running. It then uses a websocket to stream the data and is accessible via a web browser (requires a http server)

## Requirements:

numpy ; pytrigno
