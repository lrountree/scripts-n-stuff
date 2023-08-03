# Functional rcon for Ark
# Lucas Rountree, 2020
#
# Import as module or run from shell.
# 
## Request Types:
# 3: SERVERDATA_AUTH
# 2: SERVERDATA_EXECCOMMAND
## Response Types:
# 2: SERVERDATA_AUTH_RESPONSE
# 0: SERVERDATA_RESPONSE_VALUE

# Import Common Modules
import sys
import socket
from struct import pack, unpack, calcsize
#from datetime import datetime
#from log import LOG as log

# Populate variables
Buffer = 4096
#packet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Log_File = '/home/steam/3lemontrees/ShooterGame/Saved/Logs/rcon-' + datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S' + '.log'

# Set up log/exit function
#log = log('rcon_logger', Log_File, 'critical', 'debug')

# Set up socket operations as a class
class tcp:
    """Proper packet construction for Ark rcon servers.

    -- Usage --
    Command Line:
        ark_rcon.py -H <host name or ip> -P <rcon port> -p <rcon password> -c <command request>
    Module:
    import ark_rcon
    connect = ark_rcon.rcp(<host name or ip>, <rcon port>, <rcon password>)
    rcon = connect.command
    rcon(<command request>)
    or from ark_rcon import tcp; rcon = tcp(<host>, <port>, <pass>).command; rcon(<command>)

    -- Defaults --
    Host: localhost
    Port: 32330
    Pass: False (do not attempt auth)

    -- Required Input --
    Command Request
    """
    # Initialize class and grab connection/authentication values
    def __init__(self, Host = 'localhost', Port = 32330, Pass = False):
        self.packet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Host = Host
        self.Port = Port
        self.Pass = Pass
    
    # Set up function to grab rcon server response
    def get_response(self):
        """Grab server response to previous request from response stream
        If response contains data, output is:
        SIZE: response size in integer
        ID: unique request id
        TYPE: response type numerical id
        BODY: full server response message
        Otherwise, return False
        """
        Iteration = 0
        while Iteration < 11:
            Response = self.packet.recv(calcsize('<3i'))
            if len(Response) != 0:
                break
            Iteration += 1
        if Response:
            (SIZE, ID, TYPE) = unpack('<3i', Response)
            BODY = self.packet.recv(SIZE - 8)
            return (SIZE, ID, TYPE, BODY)
        else:
            return False
    
    # Ark rcon requires a very specific packet format, set up function to create and pack the packet correctly
    def create_message(self,ID,BODY,TYPE):
        """Package rcon command into format the ark server will accept
        ID: unique id for this request
        BODY: rcon command request
        TYPE: specific request type numerical id
        """
        Size = len(BODY) + 10 # get packet size
        Message = BODY.encode('utf-8') # encode message body
        return pack('<3i{0}s'.format(len(BODY)), Size, ID, TYPE, Message) + b'\x00\x00' # format the packet for the rcon server

    # Set up function to connect to and attempt authentication with the rcon server
    def auth(self):
        """Connect to rcon server, and if a password is provided then attempt to authenticate
        Output is True if successful or sys exit/server response if not
        """
        try:
            self.packet.connect((self.Host,self.Port)) # Connect to rcon host
        except:
            self.packet.close()
            return '[Connection_Response] ' + str(sys.exc_info()[1])
        else:
            Connection_Response = self.get_response()[3].decode('utf-8').rstrip('\\x00')
            if Connection_Response and 'Keep Alive' not in Connection_Response: # Check response to connection request
                self.packet.close()
                return '[Connection_Response] ' + Connection_Response
            elif not Connection_Response:
                return '[Connection_Response] Received 10 empty responses from server.'
            if self.Pass:
                try:
                    self.packet.send(self.create_message(3,self.Pass,3)) # Authenticate with rcon host
                except:
                    self.packet.close()
                    return '[Authentication Send] ' + str(sys.exc_info()[1])
                else:
                    Auth_Response = self.get_response()
                if Auth_Response and Auth_Response[1] != 3: # Check authentication response
                    self.packet.close()
                    Auth_Response_Body = Auth_Response[3].decode('utf-8').strip('\x00')
                    if not Auth_Response_Body:
                        return '[Auth_Response] Failed Authentication! Bad password?'
                    else:
                        return '[Auth_Response] ' + Auth_Response_Body
                elif not Auth_Response:
                    return '[Auth_Response] Received 10 empty responses from server.'
        return True
    
    # Set up function to send command request to rcon server
    def command(self, Command):
        """Send the specified command to the rcon server
        This is typically the only function the end user will interact with, it leverages all previous functions to perform its action
        Output will be either the server response or sys exit
        """
        Auth = self.auth()
        if Auth != True:
            self.packet.close()
            return Auth
        try:
            self.packet.send(self.create_message(2,Command,2)) # Send command request to rcon host
        except:
            self.packet.close()
            return '[Command Send] ' + str(sys.exc_info()[1])
        else:
            Send_Response = self.get_response()
        if Send_Response and Send_Response[1] != 2 or Send_Response[2] != 0: # Confirm we get the correct response, if not return an error
            self.packet.close()
            return 'Unknown error- response ID or Type does not match command request! ID: {0}, Type: {1}'.format(Send_Response[1], Send_Response[2])
        elif not Send_Response:
            self.packet.close()
            return '[Send_Response] Received 10 empty responses from server.'
        self.packet.close() # Close connection
        Send_Response_Body = Send_Response[3].decode('utf-8').strip('\x00').strip(' \n')
        return '[Send_Response] ', Send_Response_Body # Send server response, will contain response data or error data for processing later

# Run as script
if __name__ == '__main__':
    import argparse
    
    # Set up argument parser to populate values
    parser = argparse.ArgumentParser(description='Connect, authenticate with, and send commands to the Ark rcon host server.', prog='ark_rcon')
    parser.add_argument('-H', action='store', default='localhost', help='Hostname or IP address of the rcon host. Default: localhost')
    parser.add_argument('-P', action='store', default='32330', help='Port used by the host for rcon communication. Default: 32330')
    parser.add_argument('-p', action='store', default=False, help='Password to authenticate with the rcon host. Default: None')
    parser.add_argument('-c', action='store', required=True, help='Command to send to the rcon host. *Required*')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get current version of ark_rcon.py')
    args = parser.parse_args()

    rcon = tcp(args.H, int(args.P), args.p)
    Response = rcon.command(args.c)
    print(Response)
