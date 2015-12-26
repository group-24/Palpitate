CURRENT=`pwd`

SERVER=/home/app.py

HEART_RATE_DEAMON=heart_rate_server.py

CONTAINER_VIDEO=/home/server/Bill_Clinton.avi
CONTAINER_OPENCV=/opencv/

if [ "$1" = "test" ]
    then
        docker run -i -t -v $CURRENT:/home/ palpitate/palpitate-image /bin/sh -c "./run_tests.sh"
else if [ "$1" = "bash" ]
    then
        docker run -i -t -v $CURRENT:/home/ palpitate/palpitate-image /bin/bash
else
        # Startup the heart_rate_deamon and then run server
        docker run -t -p 5000:5000 -v $CURRENT:/home/ palpitate/palpitate-image /bin/bash -c "python $HEART_RATE_DEAMON $CONTAINER_OPENCV & python $SERVER $CONTAINER_VIDEO"
fi
fi


# -d flag tells docker to run image in the background
# -P flag tells docker to map container network ports to host
# Run Palpitate docker image with command to start python server
