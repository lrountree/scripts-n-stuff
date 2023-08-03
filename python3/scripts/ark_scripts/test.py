import sys, socket
from struct import unpack, calcsize
from ark_rcon import tcp
rcon = tcp('app1', 32330, 'cacadmin36').command
Results = rcon('SaveWorld')
print(Results)
#print(type(Results))
#print(Results, end='')
#print(Results[0] + Results[1])
#print(type(Results[0] + Results[1]))
#packet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
#   packet.connect(('app1', 32330))
#except:
#    sys.exc_info()[1]
#else:
#    Iteration = 0
#    while Iteration < 11:
#        Response = packet.recv(calcsize('<3i'))
#        if len(Response) != 0:
#            print('Iteration Count:', Iteration)
#            break
#        Iteration +=1
#    if Response:
#        (SIZE, ID, TYPE) = unpack('<3i', Response)
#        BODY = packet.recv(SIZE - 8)
#        print(SIZE, ID, TYPE, BODY)
#        print(packet.recv())
#    else:
#        print('False')
#packet.close()
