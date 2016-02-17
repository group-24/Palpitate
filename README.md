Palpitate - Server and research source for estimating heart rate from video and audio.

[![Build Status](https://travis-ci.org/group-24/Palpitate.svg?branch=master)](https://travis-ci.org/group-24/Palpitate)

## Repo Structure

1.   [**data_analysis**](https://github.com/group-24/Palpitate/tree/master/data_analysis): For Machine learning experiments and data preparation.

*  [**video_analysis**](https://github.com/group-24/Palpitate/tree/master/video_analysis): For Analysing video of people's faces.

*  [**server**](https://github.com/group-24/Palpitate/tree/master/server): For the flask server which hosts the video processing and applies the neural network models in real time.

*  [**palpitateDockerBuild**](https://github.com/group-24/Palpitate/tree/master/palpitateDockerBuild): Scripts for building the docker image the server is run with. Also used for Jenkins testing.

## Running the Server

1. Get the [docker quickstart terminal](https://docs.docker.com/mac/step_one/)

2. Run `./run_server.sh`. The first time you do this, the docker image for  the server should be pulled from dockerHub.

3. Wait for apporximately 6 minutes, the models for the video and and audio analysis are being made and compiled. When the log prints 'worker started' several times, the server is ready to be used

4. To access the page, use the IP adress of the docker daemon on your computer, and access port 5000


# Re-running the server

If the server crashes for some reason. use ctrl-c to cancel the process, use `docker ps` to find the process for the server and then run `docker rm -f <processID>`. This makes sure the broken server is removed from the port.
