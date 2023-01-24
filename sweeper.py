# -*- coding: utf-8 -*-
#%%
import os
import queue
import threading
import time
import tkinter as tk
import socket

#TODO add port scan

def ping(ip_address):
    command = "ping -n 1 -w 500 "
    response = os.popen(command + ip_address)
    lines = response.readlines()
    for line in lines:
        if line.count("TTL"):
            return True
    return False

def worker_task(q):
    while True:
        ip_address = q.get()
        RESULT[ip_address] = ping(ip_address)
        q.task_done()


def ping_sweep(subnet):
    q = queue.Queue()
    for i in range(255):
        worker = threading.Thread(target=worker_task,args=(q,),daemon=True)
        worker.start()
        
    for i in range(1,255):
        q.put(subnet.format(i))
    
    q.join()
    print("sweep complete")
    
    for ip in RESULT:
        if RESULT[ip]:
            print(ip,"up")

def tk_ping_sweep():
    RESULT = {}
    scan_address = entry.get()
    if len(scan_address.split("."))==4:
         subnet = ".".join(scan_address.split(".")[:-1])+".{}"
         
         ping_sweep(subnet)
    else:
        print("invalid address")


RESULT = {}

window = tk.Tk()
label = tk.Label(window,text="Enter ip Address")
label.pack()
entry = tk.Entry(window)
entry.pack()
button = tk.Button(window,text="Sweep",command=tk_ping_sweep)
button.pack()
window.mainloop()

# if len((scan_address.split("."))==4):
#     subnet = ".".join(scan_address.split(".")[:-1])+"."




