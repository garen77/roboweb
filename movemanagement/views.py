#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import time
import explorerhat

ROTATION_TIME = 20

MOTOR_STOP = 0
MOTOR_MOVE = 40
MOTOR_SLEEP = 0.5

directionRasp = 'C'


def stop():
    explorerhat.motor.one.stop()
    explorerhat.motor.two.stop()


def forward():
    explorerhat.motor.one.speed(MOTOR_MOVE)
    explorerhat.motor.two.speed(MOTOR_MOVE)
    time.sleep(MOTOR_SLEEP)
    stop()


def backward():
    explorerhat.motor.one.speed(-1 * MOTOR_MOVE)
    explorerhat.motor.two.speed(-1 * MOTOR_MOVE)
    time.sleep(MOTOR_SLEEP)
    stop()


def right():
    explorerhat.motor.one.speed(MOTOR_MOVE)
    explorerhat.motor.two.speed(-1 * MOTOR_MOVE)
    time.sleep(MOTOR_SLEEP)
    stop()


def left():
    explorerhat.motor.one.speed(-1 * MOTOR_MOVE)
    explorerhat.motor.two.speed(MOTOR_MOVE)
    time.sleep(MOTOR_SLEEP)
    stop()


mapDirection = {
    'N': forward,
    'E': right,
    'W': left,
    'S': backward,
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
