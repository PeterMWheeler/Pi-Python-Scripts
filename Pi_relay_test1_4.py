# made my ESE Jake Nielsen and ESE Peter Wheeler 2/18/25
# this script is used to control Pi headder pin to JQC3F-05VDC-c relays.
# if the device enters a error start the (Checkresult) will start a loop to hold the device in that state,

from gpiozero import LED
from time import sleep
import subprocess

GPIO_device1 = LED(24) #R1
GPIO_device2 = LED(27) #R2 
GPIO_device3 = LED(23) #R3
GPIO_device4 = LED(17) #R4
R1 = '10.200.200.1' #Ip on R1
R4 = '10.200.200.4' #Ip on R4
result = True
infin = True
count = 0


def ping(host):
    global result
    # Ping the given host and return True if it is reachable, False otherwise.
    try:
        response = subprocess.run(['ping', '-c', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # If the return code is 0, the ping was successful
        if response.returncode == 0:
           result = True
        else:
            result = False
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return False


def Checkresult(TheRouter):
    global result
    if result == True:
        print(f'Host {TheRouter} is reachable.')
    elif result == False:
        print(f'Host {TheRouter} is unreachable.')
        while infin == True:
            print(f'Test Failed. Test ran {count}-this many times')
            print(f'unending loop is running to hold device is curent state,')
            sleep(120)


while True:
    count += 1
    # Turn GPIO on before the ping test
    GPIO_device1.on()
    GPIO_device4.on()
    print('All GPIO\'s On')
    print('Soak Testing, holding state for 500 seconds')
    sleep(500)
    ping(R1)
    Checkresult(result)
    ping(R4)
    Checkresult(result)
    sleep(15)
    # Turn GPIO off after the sleep
    GPIO_device1.off()
    GPIO_device4.off()
    print('All GPIO\'s Off')
    print(f'Test {count} completed, resting 300 seconds before next test')
    sleep(300)


