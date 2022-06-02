import time
import sys

start_time = current_time = time.time() 
run_for_minutes = 10
run_for_seconds = run_for_minutes*60
max_hash = 30
hash_count = 1
add_hash = 1
bar_speed = .05

print(f'\n\n>> Example process will be running for {run_for_minutes} minutes. <<')
print(f'>> Process start time: {time.strftime("%H:%M:%S",time.localtime())} <<\n\n')

#Run progress bar for specified amount of time
while (current_time - start_time < run_for_seconds):

    #Compute bar spaces
    spaces = max_hash - hash_count

    #Progress bar
    print('\t'*4+'Running:\t['+'#'*hash_count + '.'*spaces+']', end='\r', file=sys.stdout, flush=True)

    #Change bar length and direction
    hash_count+=add_hash
    if (hash_count >= max_hash or hash_count <= 1):
        add_hash*=-1
    
    #Set progress bar speed
    time.sleep(bar_speed)

    #Update current time
    current_time = time.time()

#Process ends naturally
print('Process ended because time ran out.')
