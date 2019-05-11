'''

Created by savavel
Last modified 2019-05-11

Run remote commands on Windows Host using PyWinRM

Supported Authentication methods:
Kerberos, NTLM, Basic

Usage: 
  server    - Specifies the remote host address
  auth      - Authentication type
--username  - Auth username
--password  - Auth password
--cert      - Accepts server certificate for 
--command   - Command to run remotely


'''


import sys
import argparse
from winrm.protocol import Protocol

# Init arguments
parser = argparse.ArgumentParser(description='Windows Host remote command execution using PyWinRM')

parser.add_argument('server', type=str,
                    help='Remote server for connection')

parser.add_argument('auth', type=str,
                    help='Specified authentication type ( "kerberos", "ntlm", "basic", "certificate" )')

parser.add_argument('--username', type=str,
                    help='Username to use with NTLM/Basic Authentication')

parser.add_argument('--password', type=str,
                    help='Password to use with NTLM/Basic Authentication')

parser.add_argument('--cert', type=str,
		    help='Authentication certificate')

parser.add_argument('--command', type=str,
		    help='Command to run on Windows host e.g. "ipconfig /all"')

args = parser.parse_args()

NEW_SERVER = args.server
AUTH = args.auth
USERNAME = args.username
PASSWORD = args.password
CERT = args.cert
CMD = args.command


class RM():
    def __init__(self, transportType, account=r"", password="", certificate="" ):
        self.win_connect = Protocol(
				endpoint=NEW_SERVER,
				transport=transportType,
				username=account,
				password=password,
				server_cert_validation='ignore')

    def testAuth(self, command):
	command = command.split(" ")
	parameters = command[1:]

	shell_id = self.win_connect.open_shell()
        command_id = self.win_connect.run_command(shell_id, command[0], parameters )
        output, error_value, exit_status = self.win_connect.get_command_output(shell_id, command_id)

        self.win_connect.cleanup_command(shell_id, command_id)
        self.win_connect.close_shell(shell_id)
    
def main():
    rm = RM(AUTH, USERNAME, PASSWORD, CERT)
    rm.testAuth(CMD)

if __name__ == '__main__':
    main()
    sys.exit()
