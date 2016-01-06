import sys
import zmq
import random

def gen_data_mq(video_file, age, gender):
    socket = context.socket(zmq.DEALER)
    iden = str(random.randint(0, 1000000))
    socket.identity = iden.encode('ascii')
    socket.connect('tcp://localhost:5555')
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    socket.send_string(' '.join([video_file, age, gender]))

    sockets = dict(poll.poll(1000))
    while True:
        if socket in sockets:
            msg = socket.recv()
            if msg == 'KILL':
                break

            sys.stdout.write(msg)

    socket.close()
    context.term()

video_file = sys.argv[1]
age = sys.argv[2]
gender = sys.argv[3]

context = zmq.Context()
gen_data_mq(video_file, age, gender)

