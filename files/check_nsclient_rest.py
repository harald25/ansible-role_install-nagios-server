#!/usr/bin/env python3
import requests, json, base64, sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

(EXIT_OK, EXIT_WARNING, EXIT_CRITICAL, EXIT_UNKNOWN) = (0,1,2,3)

def main():
    try:
        #Check if correct parameters are entered

        if len(sys.argv) < 6:
            message = "Syntax error! The syntax is: [server_address] [port] [username] [password] [command] [arguments]"
            perfs = ""
            status = "UNKNOWN"

        elif len(sys.argv) == 6:
            status,message,perfs = FetchAndParse(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

        elif len(sys.argv) == 7:
            status,message,perfs = FetchAndParse(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

        else:
            message = "Syntax error! The syntax is: [server_address] [port] [username] [password] [command] [arguments]"
            perfs = ""
            status = "UNKNOWN"


        print (message, " - ", perfs)
        if status == "OK":
            sys.exit(EXIT_OK)
        elif status == "WARNING":
            sys.exit(EXIT_WARNING)
        elif status == "CRITICAL":
            sys.exit(EXIT_CRITICAL)
        elif status == "UNKNOWN":
            sys.exit(EXIT_UNKNOWN)
        else:
            print("Exit code error. Status is not set to a valid exit code")
            sys.exit(EXIT_UNKNOWN)


    except Exception as e:
        print("Error in main()")
        print (str(e))
        sys.exit(EXIT_UNKNOWN)



def SetUrl(srv_address, port, command, arguments = None):
    if arguments == None:
        return "https://" + str(srv_address) + ":" + str(port) + "/api/v1/queries/" + command + "/commands/execute_nagios"
    else:
        return "https://" + str(srv_address) + ":" + str(port) + "/api/v1/queries/" + command + "/commands/execute_nagios" + "?" + arguments

def FetchAndParse(srv_address, port, user, password, command, arguments = None):
    response = ""
    try:
        #print("lol")
        #sys.exit(EXIT_UNKNOWN)

        response = requests.get(SetUrl(srv_address, port, command, arguments), auth=(user, password), verify=False)
        data = response.json()
        #print(data)
        #sys.exit(EXIT_UNKNOWN)

        message = data["lines"][0]["message"]
        perfs = data["lines"][0]["perf"]
        status = data["result"]

        return status,message,perfs

    except Exception as e:
            print ("Error in FetchAndParse(): ", str(e))
            print (response)
            sys.exit(EXIT_UNKNOWN)

if __name__ == "__main__":
    main()
