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
                p.interval+=1


                # calculate total available memory left
                total_free_memory = 0
                for index,frames in free_memory:
                    total_free_memory+=frames

                # see if there is enough free memory for the process
                if p.req_mem <= total_free_memory:
                    # start scanning for a free spot starting at most_recent_process_end, be sure to loop around
                    # if you find one:
                    #   great, just add it into place!
                    #   aka, do the code you'll find below
                    # if you don't:
                    #   do defragmentation
                    
                    
                    # start scanning at most_recent_process_end, and if we reach the end
                    #   we have to loop around and start searching at the beginning
                    found = False
                    place_at = -1
                    for i in range(most_recent_process_end, default_number_frames):
                        for index,frames in free_memory:
                            if i == index and frames >= p.req_mem:
                                found = True
                                break
                    place_at = index
                    if not found:   # loop around
                        for i in range(most_recent_process_end):
                            for index,frames in free_memory:
                                if i == index and frames >= p.req_mem:
                                    found = True
                                    place_at = i
                                    break

                    if not found:   # do defragmentation
                        print "well shit we need to do defragmentation"
                        # we also have to update each process with its new stored at position
                        # after we do defragmentation, we record the open slot and put the
                        # next process into it!
                        # 
                        # hey make defragmentation() return the first '.' in memory so you don't
                        # have to search for it again afterwards
                        
                    print place_at

                    # ADD THE PROCESS INTO THE MEMORY
                    
                    for i in range(p.req_mem):
                        memory[place_at+i] = p.name
                    print "time %dms: Placed process %s:" % (t, p.name)
                    # do all the book keeping that needs to be done
                    p.stored_at = place_at                          # record where the process begins in memory
                    p.end_time = t + p.run_times[p.interval-1]      # set the end time of the process
                    active_processes.append(p)                      # add it to the list of active processes
                    most_recent_process_end = index + i + 1         # set most_recent_process_end
                    print_memory(memory)                            # print out the memory stack                    
                    free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                    print "free_memory: ", free_memory
                    

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
        for p in active_processes:
            if t == p.end_time:
                print "time %dms: Process %s removed:" % (t, p.name)
                for i in range(p.req_mem):                      # then actually remove it from the memory stack
                    memory[p.stored_at+i] = '.'
                proc.stored_at = -1                             # write over the previous stored at location
                print_memory(memory)                            # print out the memory stack 
                free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                print "free_memory: ", free_memory
                

        
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
    
    
    for p in processes_next_fit:
        p.print_self()

    print
    #print len(memory)

    #print_memory()

    run_next_fit(processes_next_fit)
    print
##    run_best_fit(processes_best_fit)
##    print
##    run_worst_fit(processes_worst_fit)
##    print
    

main()
