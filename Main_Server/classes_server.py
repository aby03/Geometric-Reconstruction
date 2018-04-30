import socket
import sys
import select
from threading import Thread
import os
import cv2
import numpy as np

import orb_match
import imutils

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def empty_socket(sock):
    """remove the data present on the socket"""
    input = [sock]
    sock.setblocking(0)
    while 1:
        inputready, o, e = select.select(input,[],[], 1.0)
        if len(inputready)==0: break
        for s in inputready: s.recv(1)
    sock.setblocking(1)