import pyautogui
import pygame.midi
import multiprocessing

def print_devices():
    print("Device List:")
    for n in range(pygame.midi.get_count()):
        print (n, pygame.midi.get_device_info(n))

def press_key(queue):
    while True:
        key = queue.get(block=True)
        pyautogui.press(key)

def readInput(input_device, queue):
    print("Start reading input")
    while True :
        if input_device.poll():
            event = input_device.read(1)
            if (event[0][0][0] != 248 and event[0][0][2] == 0):
                instrument_code = event[0][0][1]
                if instrument_code in drum_dict:
                    instrument = drum_dict[instrument_code]
                    print(instrument + " detected: " + str(event))
                    if instrument in keyboard_action_dict:
                        key = keyboard_action_dict[instrument]
                        #pyautogui.press(key)
                        queue.put_nowait(key)

                    if instrument == 'hi-hat pedal':
                        print("Exiting...")
                        break
    input_device.close()

drum_dict = {38: 'snare', 40: 'rim', 36: 'kick', 48: 'tom 1', 45: 'tom 2', 43: 'tom 3', 46: 'hi-hat open', 42: 'hi-hat closed', 44: 'hi-hat pedal', 23:'hi-hat release', 51: 'ride', 49: 'crash'}
keyboard_action_dict = {'tom 1': 'F', 'tom 2': 'J', 'snare': 'D', 'rim': 'K', 'tom 3': 'K', 'crash': 'left', 'ride': 'right', 'kick': 'enter', 'hi-hat open': 'esc'}

pyautogui.PAUSE = 0 # set default delay to 0

if __name__ == "__main__":

    pygame.midi.init()
    print_devices()

    print("Looking for default device:")
    device_id = pygame.midi.get_default_input_id()

    if device_id == -1:
        print("No default MIDI device!")
    else:
        my_input = pygame.midi.Input(device_id)
        print("Loading device " + str(pygame.midi.get_device_info(device_id)))

        print("Action List:")
        for key, value in keyboard_action_dict.items():
            print(key + ": " + value)
        print("Use hi-hat pedal to escape.")
        
        queue = multiprocessing.Queue()

        mp = multiprocessing.Process(target=press_key, args=(queue,), daemon=True)
        mp.start()
        readInput(my_input, queue=queue)

    pygame.midi.quit()