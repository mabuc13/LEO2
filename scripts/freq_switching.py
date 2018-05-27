import RPi.GPIO as GPIO
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--f', help='Setting the switching frequency to F', type=int)
args = parser.parse_args()

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

if __name__ == '__main__':
    print "The chosen switching frequency", args.f    
    #To go from frequency in Hz to sleep duration in seconds s = 1 / Hz
    sleep_duration = 1/args.f
    print "There we need to sleep for" , sleep_duration, "seconds before switching between low and high"
    while True:
        GPIO.output(4, True)               
        time.sleep(sleep_duration)
        GPIO.output(4, False)
        time.sleep(sleep_duration)
