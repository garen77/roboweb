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
from picamera import PiCamera
from django.http import HttpResponse
from .imagenet_classifier import classifyImage


ROTATION_TIME = 20

MOTOR_STOP = 0
MOTOR_SPEED_STEP = 20
MOTOR_SPEED_ROTATION = 40
MOTOR_MAX = 60
MOTOR_SLEEP = 0.5

directionRasp = 'C'
motorSpeed = 0
captured_image_folder = "/home/pi/roboproject/roboweb/movemanagement/static/img/"
camera = PiCamera()
camera.vflip = True

def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()
    motorSpeed = 0


def forward():
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

