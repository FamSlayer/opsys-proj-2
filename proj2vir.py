# Fuller Taylor
# Sam Suite
# Eugene Umlor

import sys

F = 3

def parsefile(filename):
	data = [int(d) for d in open(filename, 'r').read().split()]
	
	return( data )
	
def runLFU():
	print("Simulating LFU with fixed frame size of " + str(F))
	
	frames = ['.']*F
	access_t = [0]*F	#access totals
	pages = parsefile(sys.argv[1])
	pagecount = {}
	faults = 0
	
	for i in range(len(pages)):
		accessed = 0
		if pages[i] not in frames:	#page fault
			if '.' in frames:
				vic_i = frames.index('.')	#victim index of frames
				frames[vic_i] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (no victim page)")
				#todo not hardcode len of frames pls thanks
				accessed = vic_i
			else:
				#code that selects a victim
				victim = frames[0]
				
				for j in range(len(frames)):
					vic_i = frames.index(victim)
					if access_t[j] < access_t[vic_i]:
						victim = frames[j]
					elif access_t[j] == access_t[vic_i] and frames[j] < victim:
						victim = frames[j]
						
				#victim selected
				accessed = frames.index(victim)
				access_t[accessed] = 0
				
				frames[frames.index(victim)] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (victim page "+str(victim)+")")
			#increase counter of page faults
			faults += 1
		else:
			accessed = frames.index(pages[i])
		
		access_t[accessed] += 1
	print("End of LFU simulation ("+str(faults)+" page faults)")
	
def runLRU():
	print("Simulating LRU with fixed frame size of " + str(F))
	
	frames = ['.']*F
	access_t = [0]*F	#access times
	pages = parsefile(sys.argv[1])
	pagecount = {}
	faults = 0
	
	for i in range(len(pages)):
		accessed = 0
		if pages[i] not in frames:	#page fault
			if '.' in frames:
				vic_i = frames.index('.')	#victim index of frames
				frames[vic_i] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (no victim page)")
				#todo not hardcode len of frames pls thanks
				accessed = vic_i
			else:
				#code that selects a victim
				victim = frames[0]
				
				for j in range(len(frames)):
					vic_i = frames.index(victim)
					if access_t[j] > access_t[vic_i]:
						victim = frames[j]
				#victim selected
				accessed = frames.index(victim)
				
				frames[frames.index(victim)] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (victim page "+str(victim)+")")
			#increase counter of page faults
			faults += 1
		else:
			accessed = frames.index(pages[i])
		
		for j in range(len(access_t)):
			access_t[j] += 1
		access_t[accessed] = 0
	print("End of LRU simulation ("+str(faults)+" page faults)")

def runOPT():
	print("Simulating OPT with fixed frame size of " + str(F))
	
	frames = ['.']*F
	pages = parsefile(sys.argv[1])
	pagecount = {}
	faults = 0
	
	for i in range(len(pages)):
		if pages[i] not in frames:
			if '.' in frames:
				frames[frames.index('.')] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (no victim page)")
				#todo not hardcode len of frames pls thanks
				
			else:
				#select a victim
				victim = frames[0]
				for f in frames:
					if victim not in pages[i:] and f not in pages[i:]:
						if f < victim:
							victim = f
					elif f not in pages[i:]:
						victim = f
					elif victim not in pages[i:]:
						pass
					elif pages[i:].index(f) > pages[i:].index(victim):
						victim = f
					elif pages[i:].index(f) == pages[i:].index(victim) and f < victim:
						victim = f
				#victim selected
				
				frames[frames.index(victim)] = pages[i]
				print("referencing page "+str(pages[i])+" [mem: "+str(frames[0])+" "+str(frames[1])+" "+str(frames[2])+"] PAGE FAULT (victim page "+str(victim)+")")
			
			#increase counter of page faults
			faults += 1
	
	print("End of OPT simulation ("+str(faults)+" page faults)")
	
runLFU()