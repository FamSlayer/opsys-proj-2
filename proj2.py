# Fuller Taylor
# Sam Suite
# Eugene Umlor

import sys

default_frames_per_line = 32
default_number_frames = 256
t_memmove = 1


def load_input( file_name ):
    f = open(file_name, 'r').read().split('\n')
    num_processes = int(f.pop(0))
    process_list = []
    for line in f:
        info = line.split()
        name = info.pop(0)
        required_mem = int(info.pop(0))
        process_list.append(Process(name, required_mem, info))
    return process_list



# Prints the current memory stack
def print_memory( mem ):
    print '=' * default_frames_per_line

    for x in range(default_number_frames/default_frames_per_line):
        p_string = ""
        for y in range(default_frames_per_line):
            p_string += mem[ x*default_frames_per_line + y ]
        print p_string


    print '=' * default_frames_per_line



def recalculate_free_memory( mem ):
    free_list = []
    
    index = 0
    while index < len(mem):
        if mem[index] == '.':
            start = index
            count = 0
            while index < len(mem) and mem[index] == '.':
                count += 1
                index += 1
            free_list.append((start,count))
        else:
            while index < len(mem) and mem[index] != '.':
                index+=1

    return free_list

# this is the defragmentation function
# it returns the (new_memory, position of the cursor)
def defragmentation( mem, process_dictionary ):
    new_memory = ["."] * default_number_frames
    cursor = 0
    memdex = 0
    current_char = '!'
    
    while memdex < len(mem):
        while memdex < len(mem) and mem[memdex] == '.':
            memdex+=1
        if memdex >= len(mem):
            break
        
        current_char = mem[memdex]
        # set the start_at in the processes list!
        process_dictionary[current_char].stored_at = cursor
        
        while mem[memdex] == current_char:
            new_memory[cursor] = mem[memdex]
            cursor+=1
            memdex+=1
##        print "copied in %d frames" % (cursor - process_dictionary[current_char].stored_at)
##        print "current stage of defragmentation:"
##        print_memory(new_memory)

##    total_time = 0
##    p_string = ""
##    for mp in moved_processes:
##        p_string += mp.name + ", "
##        total_time += mp.req_mem * t_memmove
##    print p_string
##    print "time 760ms: Defragmentation complete (moved 210 frames: B, C, D, E, F)"
    return new_memory, cursor
    

def scan_from_cursor( cursor, free_mem, process ):
    for i in range(cursor, default_number_frames):
        for index,frames in free_mem:
            if i >= index and process.req_mem <= index + frames - i:#and frames >= p.req_mem:
                return True, i
    # if we reach here, then there isn't a slot from cursor --> end
    for i in range(cursor):
        for index,frames in free_mem:
            if i >= index and process.req_mem <= index + frames - i:#and frames >= p.req_mem:
                return True, i
    # if we reach here, then there isn't a slot from 0 --> cursor (thus need to defragment)
    return False, -1;
    

class Process:
    def __init__(self, n, mem, info):
        self.name = n
        self.req_mem = mem

        # self.interval is used to keep track of which interval the process is on
        self.interval = 0
        self.arrival_times = []
        self.run_times = []
        
        self.end_time = -1
        self.stored_at = -1

        self.parse(info)

    def parse(self,info):
        for pair in info:
            arrival_t, run_t = pair.split('/')
            self.arrival_times.append(int(arrival_t))
            self.run_times.append(int(run_t))

    def print_self(self):
        string = "arrives at |" + str(self.arrival_times[0]) + "| for |" + str(self.run_times[0]) + "|"
        for i in range(1, len(self.arrival_times)):
            string += ", and at |" + str(self.arrival_times[i]) + "| for |" + str(self.run_times[i]) + "|"
        print self.name, self.req_mem, string





##################################################################
##           THESE ARE THE FUNCTIONS OF THE PROGRAMS            ##
##      ALL HELPER FUNCTIONS AND CLASS DEFINITIONS ARE ABOVE    ##
##################################################################


def run_next_fit(processes):
    # set up the necessary pieces of the function
    
    # direct copy from the project doc:
    '''
    Note that we will only use a dynamic partitioning scheme here, meaning that your data structure
    needs to maintain a list containing (1) where each process is allocated, (2) how much contiguous
    memory each process uses, and (3) where and how much free memory is available (i.e., where each
    free partition is).
    '''

    # according to the project doc, we need to keep track of open spaces in memory and how big they are
    # (1) Well, active_processes could be a dictionary instead
    #   - But it's hard to remove entries from a dictionary
    #   - We will probably want a list of tuples?
    #       - this list will be remade after defragmentation occurs
    # (2) Already kept track of as the .req_mem member variable of each process
    # (3) We should keep track of this with a list of tuples as: [(start of gap, size of gap), etc]
    #       - this list will be remade after defragmentation occurs
    #

    # next-fit algorithm works as follows:
    '''
    For the next-fit algorithm, process Q is placed in the first free partition available found by scanning
    from the end of the most recently placed process.
    '''

    memory = ['.'] * default_number_frames
    t=0
    unfinished_processes = processes
    active_processes = []
    free_memory = [(0,default_number_frames)] #will be the initial size of free_memory
    most_recent_process_end = 0

    # ok save the processes into a dictionary of processes
    # this is really only to make defragmentation easier
    process_dict = {}
    for p in processes:
        process_dict[p.name] = p
    #print process_dict
    
    print "time %dms: Simulator started (Contiguous -- Next-Fit)" % t
    while 1:

        # 1. Check to see if any processes arrived
        #   - increase the process's interval
        #   - try to add it to memory (this will be different for each -fit algorithm)
        #       ~ if you can, do so
        #           - add it to a list of active processes
        #           - set the process's end time
        #           - update free_memory
        #       ~ if you can't, then...
        #           - check to see if there is enough total memory to run the process
        #               - if there is, then start defragmentation
        #               - if there isn't, [print] and skip this interval for the process
        #   
        #   - 
        # 2. Check to see if any processes finished
        #   - remove it from memory
        #   - update free_memory
        #   - if it is the last interval of the process, remove it from active_processes
        # 

        # 1. Check to see if any processes arrived
        processes_to_remove = []
        for p in unfinished_processes:
            if t == p.arrival_times[p.interval]:
                print "time %dms: Process %s arrived (requires %d frames)" % (t, p.name, p.req_mem)
                p.interval+=1 # whether the process gets to run or not, increase its interval count

                # calculate total available memory left
                total_free_memory = 0
                for index,frames in free_memory:
                    total_free_memory+=frames

                # see if there is enough free memory for the process
                if p.req_mem <= total_free_memory:
                    # start scanning for a free spot starting at most_recent_process_end, be sure to loop around
                    # if you don't find a slot:
                    #   do defragmentation
                    # otherwise (or after defragmentation):
                    #   great, just add it into place!
                    #   aka, do the code you'll find below
                         
                    found, place_at = scan_from_cursor(most_recent_process_end, free_memory, p)
                    
                    if not found:   # do defragmentation
                        print "time %dms: Cannot place process %s -- starting defragmentation" % (t, p.name)
                        memory, place_at = defragmentation(memory, process_dict)
                        # we also have to update each process with its new stored at position
                        #   as well as its arrival_times and end_times               

                        moved_processes = []
                        mp_string = ""      # There's a print string that we have to build
                        for frame in memory:
                            if frame != '.' and not frame in moved_processes:
                                moved_processes.append(frame)
                                mp_string+= frame + ", "

                        ## UPDATE THE ARRIVAL TIMES OF ALL THE PROCESSES THAT WERE MOVED
                        for p_name in moved_processes:
                            pc = process_dict[p_name]       # shorthanding the dictionary lookup
                            pc.end_time += place_at

                            # oh wait this should be a for loop -- all arrival times should be increased beyond pc.interval
                            if pc.interval < len(pc.arrival_times):
                                #print p_name, "before: ", pc.arrival_times[pc.interval]
                                pc.arrival_times[pc.interval] += place_at
                                #print p_name, "after: ", pc.arrival_times[pc.interval]
                      
                        t += place_at
                        print "time %dms: Defragmentation complete (moved %d frames: %s)" % (t, place_at, mp_string[:-2])
                        print_memory(memory)
                    #print place_at

                    # ADD THE PROCESS INTO THE MEMORY
                    
                    for i in range(p.req_mem):
                        memory[place_at+i] = p.name
                    print "time %dms: Placed process %s:" % (t, p.name)
                    # do all the book keeping that needs to be done
                    p.stored_at = place_at                          # record where the process begins in memory
                    p.end_time = t + p.run_times[p.interval-1]      # set the end time of the process
                    active_processes.append(p)                      # add it to the list of active processes
                    most_recent_process_end = place_at + i + 1      # set most_recent_process_end
                    print_memory(memory)                            # print out the memory stack                    
                    free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                    #print "free_memory: ", free_memory
                    #print "most_recent_process_end = ", most_recent_process_end
                    

                # there is not enough TOTAL AVAILABLE MEMORY to run this process interval
                else:
                    print "time %dms: Cannot place process %s -- skipped!" % (t, p.name)
                    print_memory(memory)                            # print out the memory stack

                
                if p.interval == len(p.arrival_times):
                    processes_to_remove.append(p)
                    
        # remove processes that are 'done' from the checking for arrived process list
        for proc in processes_to_remove:
            unfinished_processes.remove(proc);



        # 2. Check to see if any processes finished
        # 2. Check to see if any processes finished
        processes_to_remove = []
        for p in active_processes:
            if t == p.end_time:
                #print "length of active_processes is: ", len(active_processes)
                print "time %dms: Process %s removed:" % (t, p.name)
                for i in range(p.req_mem):                      # then actually remove it from the memory stack
                    memory[p.stored_at+i] = '.'
                p.stored_at = -1                                # write over the previous stored at location
                print_memory(memory)                            # print out the memory stack 
                free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                processes_to_remove.append(p)
                #print "free_memory: ", free_memory
                
        # remove processes from the active_processes once they are finished!
        for proc in processes_to_remove:
            active_processes.remove(proc)

        if len(processes_to_remove) > 0:
            #print "number of unfinished_processes = ", len(unfinished_processes)
            #print "number of active_processes = ", len(active_processes)
            if len(unfinished_processes) == 0 and len(active_processes) == 0:
                break
            
        if t > 9999: # just to prevent the infinite loop
            break
        t+=1
        

    print "time %dms: Simulator ended (Contiguous -- Next-Fit)" % t





def main():

    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of input arguments!"
        return

    in_file = sys.argv[1]

    # create unique lists of processes, so that each function runs with fresh processes
    processes_next_fit = load_input(in_file)
    processes_best_fit = load_input(in_file)
    processes_worst_fit = load_input(in_file)
    processes_virtual = load_input(in_file)
    
    
##    for p in processes_next_fit:
##        p.print_self()
##
##    print
    #print len(memory)

    #print_memory()

    # this test case was to test 
##    list_string = "................................AAAAAAAAAAAA.BBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD.........................EEEEEEEEEEEEEEFFFFFFFFFFFFFFFFFFFFFFFF."
##    memory1 = []
##    for i in list_string:
##        memory1.append(i)
##    print_memory(memory1)
##    
##
##    new_mem,cursor = defragmentation(memory1)
##    print_memory(new_mem)
##    print new_mem[cursor-1]
    #print "at start: number of processes = ", len(processes_next_fit)
    
    run_next_fit(processes_next_fit)
    print
##    run_best_fit(processes_best_fit)
##    print
##    run_worst_fit(processes_worst_fit)
##    print
    

main()
