from asyncio import subprocess
from signal import signal
import time
import subprocess
import wmi
import PySimpleGUI as sg

kill_list = ['example_process.py']
batch_files_to_execute = ['C:/Users/jjaso/Desktop/Python/tensorflowEnv/deployment-timeout/Examples/example_process.bat']

max_pause_time = 60 #minutes 
min_pause_time = 1 #minutes
default_pause_time = 30 #minutes

title_font = ('Arial, 18')
paragraph_font = ('Arial, 12')

start_time = time.time()
timer_on = False
pause_time = default_pause_time


layout_pre_process = [
    [sg.Text('Control your Privacy', size=(60,1), justification='center', pad=(1,30), font=title_font)],
    [   
        sg.Text('Specify amount of time to terminate deployment (minutes)', 
            size=(60,1), 
            justification='center', 
            font=paragraph_font,
            key='-TerminateSliderText-')],
    [       
        sg.Slider((min_pause_time,max_pause_time),
            default_pause_time,
            1, 
            orientation='h', 
            size=(30,20),
            key='-TerminateTimeSlider-',
            font=paragraph_font)
    ],
    [sg.Button('Stop Deployment', key='-StopDeploymentBtn-', pad=(1,30), font=paragraph_font)],
    [sg.Text('', key='-TimerDisplay-', size=(60,1), justification='center', pad=(1,30), font=paragraph_font, text_color='red')]
]

layout = [[sg.Column(layout_pre_process, element_justification='center')]]

window = sg.Window(title="Deployment Control Panel", layout=layout, margins = (10,50))

def start_timer():
    global start_time, timer_on
    
    start_time = time.time()
    timer_on = True

def get_start_time():
    return start_time

def get_current_time():
    return time.time()

def check_timer():
    global timer_on 
    if not ((get_current_time() - get_start_time()) < (pause_time*60)):
        timer_on = False   

def get_time_left():
    seconds_left = (pause_time*60) - (get_current_time() - get_start_time())
    return time.strftime("%M:%S", time.gmtime(seconds_left))

def terminate_process():
    global window

    #Start Timer
    start_timer()

    #Update Window to remove elements
    make_elements_invisible_before_terimination()
    window.refresh()

    #Terminate all process
    terminate_running_processes()

    #Display Time
    while timer_on:
        window['-TimerDisplay-'].update(f'Deployment is terminated for the next {get_time_left()} minutes')
        time.sleep(.5)
        window.refresh()
        check_timer()

    #Update window to add elements
    make_elements_visible_after_terimination()

    restart_batch_files()

def terminate_running_processes():
    '''Search all running processes and terminate python script processes in kill list'''

    for process_name_to_kil in kill_list:
        try:
            f = wmi.WMI()
            for process in f.WIN32_Process():
                #Could be None
                if process.CommandLine:
                    if process_name_to_kil in process.CommandLine:
                        process.Terminate()
        except Exception as e:
            print('Termination Error: ', e)

def restart_batch_files():
    for batch_file in batch_files_to_execute:
        try:
            subprocess.call([batch_file])
        except Exception as e:
            print('Restart error for ',batch_file, 'Error:',e)
        

def make_elements_visible_after_terimination():
    global window
    window['-StopDeploymentBtn-'].update(disabled=False)
    window['-StopDeploymentBtn-'].update(visible=True)
    window['-TerminateSliderText-'].update(visible=True)
    window['-TerminateTimeSlider-'].update(visible=True)
    window['-TimerDisplay-'].update(visible=False)

def make_elements_invisible_before_terimination():
    global window
    window['-StopDeploymentBtn-'].update(disabled=True)
    window['-StopDeploymentBtn-'].update(visible=False)
    window['-TerminateSliderText-'].update(visible=False)
    window['-TerminateTimeSlider-'].update(visible=False)
    window['-TimerDisplay-'].update(visible=True)


while True:
    event, values = window.read()

    if event == '-StopDeploymentBtn-':
        #Get amount of time to terminate deployment
        pause_time = int(float(values['-TerminateTimeSlider-']))
        #Terminate deployment
        terminate_process()
    
    if event == sg.WIN_CLOSED:
        break 

window.close()
    