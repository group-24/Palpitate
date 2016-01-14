Palpitate - Machine Learning thingy

[![Build Status](https://travis-ci.org/group-24/Palpitate.svg?branch=master)](https://travis-ci.org/group-24/Palpitate)

## Running the Server

1. Get the [docker quickstart terminal](https://docs.docker.com/mac/step_one/)
2. Run `./run_server.sh`. The first time you do this, the docker image for the server should be pulled from dockerHub.
3. Wait for apporximately 6 minutes, the models for the video and and audio analysis are being made and compiled. When the log prints 'worker started' several times, the server is ready to be used
4. To access the page, use the IP adress of the docker daemon on your computer, and access port 5000


# Re-running the server

If the server crashes for some reason. use ctrl-c to cancel the process, use `docker ps` to find the process for the server and then run `docker rm -f <processID>`. This makes sure the broken server is removed from the port.
