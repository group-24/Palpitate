CURRENT=`pwd`

SERVER=/home/app.py
CONTAINER_VIDEO=/home/server/Bill_Clinton.avi
CONTAINER_OPENCV=/opencv/

#

if [ "$1" = "test" ]
    then
        docker run -i -t -v $CURRENT:/home/ palpitate/palpitate-image /bin/sh -c "./run_tests.sh"
else if [ "$1" = "bash" ]
    then
        docker run -i -t -v $CURRENT:/home/ palpitate/palpitate-image /bin/bash
else
        # run the server
        docker run -p 5000:5000 -v $CURRENT:/home/ palpitate/palpitate-image python $SERVER $CONTAINER_VIDEO $CONTAINER_OPENCV
fi
fi


# -d flag tells docker to run image in the background
# -P flag tells docker to map container network ports to host
# run Palpitate docker image with command to start python server
