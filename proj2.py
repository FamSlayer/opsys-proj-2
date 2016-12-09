# Fuller Taylor
# Sam Suite
# Eugene Umlor

import sys

default_frames_per_line = 32
default_number_frames = 256
memory = ['.'] * default_number_frames

def print_memory( ):
    print '=' * default_frames_per_line

    for x in range(default_number_frames/default_frames_per_line):
        p_string = ""
        for y in range(default_frames_per_line):
            p_string += memory[ x*default_frames_per_line + y ]
        print p_string


    print '=' * default_frames_per_line


def main():

    if len(sys.argv) != 3:
        print "ERROR: Incorrect number of input arguments!"
        return


    in_file = sys.argv[1]
    out_file = sys.argv[2]

    print in_file
    print out_file

    print len(memory)

    print_memory()
    

main()
