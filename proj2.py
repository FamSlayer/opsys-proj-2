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


# returns a list of tuples
# [ (start1, #frames1), (start2, #frames2), (startN, #framesN) ]
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
    moved_procs = []
    non_moved_procs = []
    while memdex < len(mem):
        while memdex < len(mem) and mem[memdex] == '.':
            memdex+=1
        if memdex >= len(mem):
            break
        
        current_char = mem[memdex]
        # set the start_at in the processes list!
        process_dictionary[current_char].stored_at = cursor
        if cursor != memdex:
            moved_procs.append(current_char)
        else:
            non_moved_procs.append(current_char)
        while mem[memdex] == current_char:
            new_memory[cursor] = mem[memdex]
            cursor+=1
            memdex+=1

    # for any processes that actually didn't move at all
    time_saved = 0
    for proc in non_moved_procs:
        time_saved = process_dictionary[proc].req_mem * t_memmove
    return new_memory, cursor, moved_procs, time_saved
    
# next-fit algorithm
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


# best-fit helper function
def find_smallest_valid_partition( free_mem, process ):
    #print free_mem
    if len(free_mem) == 1:
        return True, free_mem[0][0]
    # ok now we have to do the real testing!
    # loop through all the gaps in free memory
    #   if memory + process.req_mem <= frames:
    #       if frames < smallest:
    #           location, smallest = 
    smallest_size = default_number_frames
    smallest_loc = -1
    found = False
    for index,frames in free_mem:
        if process.req_mem <= frames:
            if frames < smallest_size:
                found = True
                smallest_size = frames
                smallest_loc = index

    if found:
        return True, smallest_loc
    return False, -1
    

# worst-fit helper function
def find_largest_valid_partition( free_mem, process):
    #print free_mem
    if len(free_mem) == 1:
        return True, free_mem[0][0]
    found = False
    largest_size = 0
    largest_loc = -1
    for index,frames in free_mem:
        if process.req_mem <= frames:
            if frames > largest_size:
                found = True
                largest_size = frames
                largest_loc = index

    if found:
        return True, largest_loc
    return False, -1

    

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


def run_contiguous_fit(processes, fit_type):
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
    # best-fit algorithm works as follows:
    '''
    For the best-fit algorithm, process Q is placed in the smallest free partition available in which
    process Q fits. If a "tie" occurs, use the free partition closer to the "top" of memory.
    '''
    # worst-fit algorithm works as follows:
    '''
    For the worst-fit algorithm, process Q is placed in the largest free partition available in which
    process Q fits. If a "tie" occurs, use the free partition closer to the "top" of memory.
    '''
    

    memory = ['.'] * default_number_frames
    t=0
    unfinished_processes = processes
    active_processes = []
    free_memory = [(0,default_number_frames)] #will be the initial size of free_memory
    most_recent_process_end = 0

    # ok save the processes into a dictionary of processes
    # this is to make the defragmentation step easier
    process_dict = {}
    for p in processes:
        process_dict[p.name] = p
    
    
    print "time %dms: Simulator started (Contiguous -- %s)" % (t, fit_type)
    while 1:

        # 1. Check to see if any processes arrived
        #   - increase the process's interval
        #   - try to add it to memory (this will be different for each -fit algorithm)
        #       ~ if there is enough total available memory
        #           ~ scan for an opening from the placed cursor
        #               - if you find one, save the location
        #               - if there isn't one, we need to defragment
        #           ~ after the location is found (whether defragmented or not)
        #               - place the process at the location 
        #       ~ if you can't, skip the process
        #           - but increase its interval incase it can fit in when it comes back
        # 2. Check to see if any processes finished
        #   - remove it from memory
        #   - update free_memory
        #   - if it is the last interval of the process, remove it from active_processes
        #


        # 2. CHECK TO SEE IF ANY PROCESSES FINISHED
        # alphabetize them first...
        names = []
        for proc in active_processes:
            names.append(proc.name)
        names.sort()
        alphabetized_active_processes = []
        for n in names:
            alphabetized_active_processes.append(process_dict[n])

        # removing processes that are done
        # our program will be done after removing a process
        # so the end check needs to see if the size of this is > 0
        processes_to_remove1 = []
        for p in alphabetized_active_processes:
            if t == p.end_time:
                print "time %dms: Process %s removed:" % (t, p.name)
                for i in range(p.req_mem):                      # then actually remove it from the memory stack
                    memory[p.stored_at+i] = '.'
                p.stored_at = -1                                # write over the previous stored at location
                print_memory(memory)                            # print out the memory stack 
                free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                processes_to_remove1.append(p)
                
        # remove processes from the active_processes once they are finished!
        for proc in processes_to_remove1:
            active_processes.remove(proc)
        

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

                ## IF THERE IS ENOUGH TOTAL AVAILABLE MEMORY FOR THE PROCESS
                if p.req_mem <= total_free_memory:
                    # start scanning for an open slot
                    
                    found, place_at = None, None
                    if fit_type == "Next-Fit":
                        found, place_at = scan_from_cursor(most_recent_process_end, free_memory, p)
                    elif fit_type == "Best-Fit":
                        found, place_at = find_smallest_valid_partition(free_memory, p)
                    elif fit_type == "Worst-Fit":
                        found, place_at = find_largest_valid_partition(free_memory, p)

                    
                    if not found:   # do defragmentation
                        print "time %dms: Cannot place process %s -- starting defragmentation" % (t, p.name)
                        memory, place_at,moved_processes,time_saved = defragmentation(memory, process_dict)
                        
                        # we also have to update each process with its new stored at position
                        #   as well as its arrival_times and end_times               
                        mp_string = ""      # There's a print string that we have to build
                        for proc in moved_processes:
                            mp_string+= proc + ", "

                        time_defragmented = place_at * t_memmove - time_saved
                        ## UPDATE THE ARRIVAL TIMES && END TIMES OF ALL THE PROCESSES THAT WERE MOVED
                        for p_name in process_dict:
                            pc = process_dict[p_name]
                            if pc.end_time >= t:
                                pc.end_time += time_defragmented

                            # oh wait this should be a for loop -- all arrival times should be increased beyond pc.interval
                            if pc.interval < len(pc.arrival_times):
                                for intrvl in range(pc.interval,len(pc.arrival_times)):
                                    pc.arrival_times[intrvl] += time_defragmented
                        # officially increase the time, and then print
                        t += time_defragmented
                        print "time %dms: Defragmentation complete (moved %d frames: %s)" % (t, time_defragmented, mp_string[:-2])
                        print_memory(memory)

                    ## ADD THE PROCESS INTO THE MEMORY
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

                # there is not enough TOTAL AVAILABLE MEMORY to run this process interval
                else:
                    print "time %dms: Cannot place process %s -- skipped!" % (t, p.name)
                    print_memory(memory)                            # print out the memory stack

                # if it is the last time a process will arrive
                if p.interval == len(p.arrival_times):
                    processes_to_remove.append(p)
                    
        # remove processes that are 'done' from the checking for arrived process list
        # This step is necessary because you can't modify the list you're looping through!
        for proc in processes_to_remove:
            unfinished_processes.remove(proc);


       

        # do the end check for the program
        if len(processes_to_remove1) > 0:
            if len(unfinished_processes) == 0 and len(active_processes) == 0:
                break

        # FAILSAFE TO PREVENT AN INFINITE LOOP
        #if t > 99999:
        #    break
        
        t+=1
        
    # the simulator is over. Print that!
    print "time %dms: Simulator ended (Contiguous -- %s)" % (t, fit_type)


def run_noncontiguous(processes):
    # direct copy from the project doc:
    '''
    To place pages into frames of physical memory, use a simple first-fit approach.
    '''

    memory = ['.'] * default_number_frames
    t=0
    unfinished_processes = processes
    active_processes = []
    free_memory = [(0,default_number_frames)] #will be the initial size of free_memory
    most_recent_process_end = 0

    # ok save the processes into a dictionary of processes
    process_dict = {}
    for p in processes:
        process_dict[p.name] = p
    
    
    print "time %dms: Simulator started (Non-contiguous)" % t
    while 1:


        # 1. Check to see if any processes finished
        #   - remove it from memory
        #   - update free_memory
        #   - if it is the last interval of the process, remove it from active_processes
        #
        # 2. Check to see if any processes arrived
        #   - increase the process's interval
        #   - try to add it to memory
        #       ~ if there is enough total available memory
        #           - scan for openings from the beginning
        #               - if you find one, place as much of the process as you can in the available memory
        #               - continue until all memory has been placed
        #       ~ if you can't, skip the process
        #           - but increase its interval incase it can fit in when it comes back


        # 1. CHECK TO SEE IF ANY PROCESSES FINISHED
        # alphabetize them first...
        names = []
        for proc in active_processes:
            names.append(proc.name)
        names.sort()
        alphabetized_active_processes = []
        for n in names:
            alphabetized_active_processes.append(process_dict[n])

        # removing processes that are done
        # our program will be done after removing a process
        # so the end check needs to see if the size of this is > 0
        processes_to_remove1 = []
        for p in alphabetized_active_processes:
            if t == p.end_time:
                print "time %dms: Process %s removed:" % (t, p.name)
                for i in range(len(memory)):                    # then actually remove it from the memory stack
                    if (memory[i] == p.name):
                        memory[i] = '.'
                
                p.stored_at = -1                                # write over the previous stored at location
                print_memory(memory)                            # print out the memory stack 
                free_memory = recalculate_free_memory(memory)   # recalculate the free_memory
                processes_to_remove1.append(p)
                
        # remove processes from the active_processes once they are finished!
        for proc in processes_to_remove1:
            active_processes.remove(proc)
        

        # 2. Check to see if any processes arrived
        processes_to_remove = []
        for p in unfinished_processes:
            if t == p.arrival_times[p.interval]:
                print "time %dms: Process %s arrived (requires %d frames)" % (t, p.name, p.req_mem)
                p.interval+=1 # whether the process gets to run or not, increase its interval count

                # calculate total available memory left
                total_free_memory = 0
                for index,frames in free_memory:
                    total_free_memory+=frames

                ## IF THERE IS ENOUGH TOTAL AVAILABLE MEMORY FOR THE PROCESS
                if p.req_mem <= total_free_memory:
                    # start scanning for an open slot

                    placed_memory = 0
                    #   ~ scan for openings from the beginning
                    for index,frames in free_memory:
                        for i in range(index, index+frames):
                            if (placed_memory < p.req_mem):
                                # - place as much of the process as you can in the available memory
                                memory[i] = p.name
                                placed_memory += 1
                                
                            # - continue until all memory has been placed
                            else:
                                break
                        if (placed_memory >= p.req_mem):
                            break


                    print "time %dms: Placed process %s:" % (t, p.name)
                    # do all the book keeping that needs to be done
                    p.end_time = t + p.run_times[p.interval-1]      # set the end time of the process
                    active_processes.append(p)                      # add it to the list of active processes
                    print_memory(memory)                            # print out the memory stack                    
                    free_memory = recalculate_free_memory(memory)   # recalculate the free_memory

                # there is not enough TOTAL AVAILABLE MEMORY to run this process interval
                else:
                    print "time %dms: Cannot place process %s -- skipped!" % (t, p.name)
                    print_memory(memory)                            # print out the memory stack

                # if it is the last time a process will arrive
                if p.interval == len(p.arrival_times):
                    processes_to_remove.append(p)
                    
        # remove processes that are 'done' from the checking for arrived process list
        # This step is necessary because you can't modify the list you're looping through!
        for proc in processes_to_remove:
            unfinished_processes.remove(proc);


        # do the end check for the program
        if len(processes_to_remove1) > 0:
            if len(unfinished_processes) == 0 and len(active_processes) == 0:
                break

        # FAILSAFE TO PREVENT AN INFINITE LOOP
        #if t > 99999:
        #    break
        
        t+=1
        
    # the simulator is over. Print that!
    print "time %dms: Simulator ended (Non-contiguous)" % t




def main():

    if len(sys.argv) != 2:
        print "ERROR: Incorrect number of input arguments!"
        return

    in_file = sys.argv[1]

    # create unique lists of processes, so that each function runs with fresh processes
    processes_next_fit = load_input(in_file)
    processes_best_fit = load_input(in_file)
    processes_worst_fit = load_input(in_file)
    processes_noncontiguous = load_input(in_file)
    processes_virtual = load_input(in_file)
    

    run_contiguous_fit(processes_next_fit, "Next-Fit")
    print
    run_contiguous_fit(processes_best_fit, "Best-Fit")
    print
    run_contiguous_fit(processes_worst_fit, "Worst-Fit")
    print
    run_noncontiguous(processes_noncontiguous)
    

main()
