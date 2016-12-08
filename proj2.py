# Fuller Taylor
# Sam Suite
# Eugene Umlor

import sys


def main():

    if len(sys.argv) != 3:
        print "ERROR: Incorrect number of input arguments!"
        return


    in_file = sys.argv[1]
    out_file = sys.argv[2]

    print in_file
    print out_file
    

main()
