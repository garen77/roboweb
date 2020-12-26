#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import time
import explorerhat
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
from django.http import HttpResponse
import threading
from .imagenet_classifier import classifyImage

PIN_TRIGGER_LEFT = 18
PIN_ECHO_LEFT = 8
PIN_ECHO_RIGHT = 1
PIN_TRIGGER_RIGHT = 7

#PIN_TRIGGER_LEFT = 7
#PIN_ECHO_LEFT = 1
#PIN_ECHO_RIGHT = 8
#PIN_TRIGGER_RIGHT = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(PIN_ECHO_LEFT, GPIO.IN)

GPIO.setup(PIN_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(PIN_ECHO_RIGHT, GPIO.IN)

ROTATION_TIME = 20

MOTOR_STOP = 0
MOTOR_SPEED_STEP = 20
MOTOR_SPEED_ROTATION = 30
MOTOR_MAX = 40
MOTOR_SLEEP = 0.20

MINIMUM_DISTANCE = 10

directionRasp = 'C'
motorSpeed = 0
captured_image_folder = "/home/pi/roboproject/roboweb/movemanagement/static/img/"
camera = PiCamera()
camera.vflip = True

selfDrivingactive = False

pulse_start_time = time.time()
pulse_end_time = time.time()
left_distance = 10
right_distance = 10

def thread_distance(name):
    try:
        while True:
            global pulse_start_time
            global pulse_end_time			
            global left_distance
            global right_distance

            print("--------Start distance rilevation thread ",name)
            GPIO.output(PIN_TRIGGER_LEFT, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(PIN_TRIGGER_LEFT, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER_LEFT, GPIO.LOW)
            while GPIO.input(PIN_ECHO_LEFT)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO_LEFT)==1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            left_distance = round(pulse_duration * 17150, 2)
            print("--------Left Distance:",left_distance," cm")
            GPIO.output(PIN_TRIGGER_RIGHT, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(PIN_TRIGGER_RIGHT, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER_RIGHT, GPIO.LOW)
            while GPIO.input(PIN_ECHO_RIGHT)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO_RIGHT)==1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            right_distance = round(pulse_duration * 17150, 2)
            print("--------Right Distance:",right_distance," cm")
            print("--------End distance rilevation thread ",name)
    finally:
        GPIO.cleanup()


def thread_self_driving(name):
    global selfDrivingactive
    while True:
        if selfDrivingactive:
            forward()
            time.sleep(MOTOR_SLEEP)


def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()
    motorSpeed = 0


def forward():
    i = 0
    while i < 5 and (left_distance < MINIMUM_DISTANCE or right_distance < MINIMUM_DISTANCE):
        obstacle_avoid()
    global motorSpeed
    if motorSpeed <= 0:
        motorSpeed = MOTOR_SPEED_STEP
    elif motorSpeed < MOTOR_MAX:
        motorSpeed = motorSpeed + MOTOR_SPEED_STEP
    else:
        motorSpeed = MOTOR_MAX
    explorerhat.motor.one.speed(motorSpeed)
    explorerhat.motor.two.speed(motorSpeed)
    time.sleep(MOTOR_SLEEP)
    stop()


def backward():
    global motorSpeed
    if motorSpeed >= 0:
        motorSpeed = -1 * MOTOR_SPEED_STEP
    elif motorSpeed > MOTOR_MAX:
        motorSpeed = motorSpeed - MOTOR_SPEED_STEP
    else:
        motorSpeed = -1 * MOTOR_MAX
    explorerhat.motor.one.speed(motorSpeed)
    explorerhat.motor.two.speed(motorSpeed)
    time.sleep(MOTOR_SLEEP)
    stop()


def right():
    explorerhat.motor.one.speed(MOTOR_SPEED_ROTATION)
    explorerhat.motor.two.speed(-1 * MOTOR_SPEED_ROTATION)
    time.sleep(MOTOR_SLEEP)
    stop()


def left():
    explorerhat.motor.one.speed(-1 * MOTOR_SPEED_ROTATION)
    explorerhat.motor.two.speed(MOTOR_SPEED_ROTATION)
    time.sleep(MOTOR_SLEEP)
    stop()

def obstacle_avoid():
    backward()
    if left_distance < MINIMUM_DISTANCE:
        right()
    elif right_distance < MINIMUM_DISTANCE:
        left()


mapDirection = {
    'N': forward,
    'E': right,
    'W': left,
    'S': backward,
    'NE': right,
    'NW': left,
    'SE': right,
    'SW': left,
    'C': stop,
    }


# Create your views here.

def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable

    return render(request, 'index.html')


@api_view(['GET', 'POST'])
def heartBeat(request):
    if request.method == 'GET':
        return JsonResponse({'direction': directionRasp})
    return Response({'message': 'moveUp'})


@api_view(['GET', 'POST'])
def move(request):
    if request.method == 'POST':
        direction = request.POST.get('direction')
        if direction is not None:
            mapDirection[direction]()
            directionRasp = direction
            return JsonResponse({'direction': direction})
        else:
            return JsonResponse({'direction': 'null'})
    return Response({'message': 'move'})


@api_view(['GET', 'POST'])
def recognize(request):
    if request.method == 'GET':
        camera.start_preview()
        time.sleep(1)
        camera.capture(captured_image_folder + 'image.jpg')
        camera.stop_preview()
        res = classifyImage()
        image_data = base64.b64encode(open(captured_image_folder+"image.jpg", "rb").read()).decode('utf-8')
        classified = str(res[0]) + " " + str(res[1])
        return JsonResponse({'recognized': classified, 'imagerecognized': image_data})
    return JsonResponse({'recognized': 'nothing'})        

@api_view(['GET', 'POST'])
def selfDriving(request):
    global selfDrivingactive
    if request.method == 'POST':
        selfdriving = request.POST.get('selfdriving') 
        if selfdriving == '1':
            selfDrivingactive = True
            print("######### thread started selfdriving ",selfdriving)
        elif selfdriving == '0':
            selfDrivingactive = False
            print("######### thread stopped selfdriving ",selfdriving)
        else:
            print("######### thread state not started and not stopped selfdriving ",selfdriving)
        return JsonResponse({'selfdriving': selfdriving})		
    return JsonResponse({'selfdriving': '0'})

td = threading.Thread(target=thread_distance, args=(1,))
td.start()

tsd = threading.Thread(target=thread_self_driving, args=(2,))
tsd.start()