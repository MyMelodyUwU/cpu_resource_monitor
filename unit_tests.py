#!usr/bin/env python3

import os
import platform
import psutil

def main():
    
    return 0

def check_cpu(list_of_temps):
    #assert(type(list_of_temps) == "list")

    return 0

def check_json():

    return 0    

def test_serve_page(content):
    assert(type(content) == list)

    return 0    

def test_cpu_specs(cpu_architecture):

    assert(cpu_architecture["count"], psutil.cpu_count(logical=False))
    assert(cpu_architecture["processor_type"], platform.processor())
    assert(cpu_architecture["host_name"], os.uname()[1])
    
    return 0


if __name__ == '__main__':
    main()
