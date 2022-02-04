#!/usr/bin/python

from socket import *
import optparse
from threading import *
from colorama import Fore

# ConnScan FUNCTION


def connScan(THOST, TPORT):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((THOST, TPORT))
        print(
            f'{Fore.LIGHTBLUE_EX}[+] -> {TPORT}/TCP --> {Fore.LIGHTGREEN_EX}OPEN')
    except:
        print(
            f'{Fore.LIGHTBLUE_EX}[-] -> {TPORT}/TCP --> {Fore.LIGHTRED_EX} CLOSE')
    finally:
        sock.close()


# RETRIEVE BANNER FROM OPEN PORTS
def retBanner(T_PORT, THOST):
    try:
        # CHECK IF THE -B OPTION NULL OR EMPTY
        if T_PORT == None or T_PORT == "":
            pass

        # SET DEFAULT TIME OUT TO --> 2 SECONDS
        setdefaulttimeout(2)
        SOCK_1 = socket()
        SOCK_1.connect((THOST, int(T_PORT)))
        BANNER = SOCK_1.recv(1024)  # BANNER PAYLOAD
        return BANNER
    except:
        print(
            f"==================BANNER RESULT ON PORT: {Fore.LIGHTGREEN_EX}{T_PORT}/TCP ==================")
        print(
            f'{Fore.LIGHTMAGENTA_EX}[!] - BANNER NOT RETRIVED ON PORT: {T_PORT}')
        print(
            f"====================================================================")


# PORT SCANNER FUNCTION
def PortScan(THOST, TPORTS):

    # RESOLVE TARGET HOST TO IP
    TARGET_IP = ''
    TARGET_NAME = ''
    try:
        TARGET_IP = gethostbyname(THOST)
    except:
        print(f'{Fore.LIGHTYELLOW_EX}[!] --> Unknown Target Host')
    # REVERSE IP LOOKUP / RESOLVE IP TO HOSTNAME
    try:
        TARGET_NAME = gethostbyaddr(TARGET_IP)
        print(f'{Fore.LIGHTGREEN_EX}[+] Scan Results For: {TARGET_NAME[0]}')
    except:
        print(f'{Fore.LIGHTGREEN_EX}[+] Scan Results For: {TARGET_IP}')
    setdefaulttimeout(1)
    for PORT in TPORTS:
        th = Thread(target=connScan, args=(THOST, int(PORT)))
        th.start()


def main():
    parser = optparse.OptionParser(
        f'Usage of Program: \n [++] -H {Fore.LIGHTGREEN_EX}<TARGET HOST> -p {Fore.LIGHTMAGENTA_EX}<TARGET PORTS> -B (--banner) {Fore.LIGHTGREEN_EX}<TARGET OPEN PORTS>')
    parser.add_option('-H', dest="THOST", type="string",
                      help="PROVIDE TARGET HOST (!IMPORTANT)")
    parser.add_option('-p', dest="TPORTS", type="string",
                      help="PROVIDE TARGET PORTS SEPARATED BY COMMA")
    parser.add_option('-B', dest='T_Banner', type="string",
                      help="RETRIEVE BANNER FROM OPEN PORTS")
    (options, args) = parser.parse_args()

    # CHECK IF THE GIVEN ARGS ARE EMPTY VALUES
    if (options.THOST == None) and (options.TPORTS == None) and (options.T_Banner == None):
        print(f'{Fore.LIGHTCYAN_EX}{parser.usage}')
        exit(0)

    THOST = options.THOST
    TPORTS = options.TPORTS.split(',')

    # CHECK IF THE --BANNER OPTIONS INCLUDED
    # if not(options.T_Banner) or options.T_Banner == None:
    ###   print(f'{Fore.LIGHTYELLOW_EX}[!] -> Banner Option (-B) Not Provided!')

    PortScan(THOST, TPORTS)
    # LOOP THROUGH ON PROVIDED PORTS
    for PORT in TPORTS:
        BANNER_RES = retBanner(PORT, THOST)
        if BANNER_RES:
            print(
                f"==================BANNER RESULT ON PORT: {Fore.LIGHTGREEN_EX}{PORT}/TCP ==================")
            print(f'{Fore.LIGHTGREEN_EX}[+] IP: {THOST}: {BANNER_RES}')
            print(
                f"=================================================================================================")
        else:
            print(
                f'{Fore.LIGHTYELLOW_EX}[!] -> Banner Option (-B) Not Provided!')


if __name__ == "__main__":
    main()
