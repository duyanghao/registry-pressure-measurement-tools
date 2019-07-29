#!/usr/bin/python

from subprocess import Popen, PIPE
from time import time
from time import sleep
from threading import Thread
from Queue import Queue
import os
import argparse

begin = 1
iterations = 100
concurrency = 100
repo_address = "your-docker-registry-domain"

repo_ref = "/test-1"
repo_url = repo_address + repo_ref
container_name = "nginx"
work_dir = "containers/nginx"
build_results_file = "build_results.csv"
push_results_file = "push_results.csv"
pull_results_file = "pull_results.csv"
delete_local_results_file = "delete_local_results.csv"

results_files = [pull_results_file]

for results_file in results_files:
    outfile = open(results_file, 'w')
    outfile.write("iteration,succeed or not,spent_time")
    outfile.close()

work_queue = Queue()

imagePrefix = repo_url + '/' + container_name + ':v'

def build_container(iteration):
    start_time = time()
    build_command = Popen(['docker', 'build', '--no-cache=true', '-t', imagePrefix + str(iteration), '--file=' + work_dir + '/dockerfile', work_dir])
    ret_code = build_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(build_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

def push_container(iteration):
    start_time = time()
    push_command = Popen(['docker', 'push', imagePrefix + str(iteration)])
    ret_code = push_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(push_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

def delete_local_images(iteration):
    start_time = time()
    delete_local_images_command = Popen(['docker', 'rmi', imagePrefix + str(iteration)])
    ret_code = delete_local_images_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(delete_local_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()


def pull_container(iteration):
    start_time = time()
    pull_command = Popen(['docker', 'pull', imagePrefix + str(iteration)])
    ret_code = pull_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(pull_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

def repeat():
    if work_queue.empty() is False:
        iteration = work_queue.get_nowait()
        container_action(iteration)
        work_queue.task_done()


def fill_queue(iterations):
    for iteration in range(begin, (iterations + 1)):
        work_queue.put(iteration)

#container_actions = [build_container, push_container, delete_local_images, pull_container]
container_actions = [pull_container]

for container_action in container_actions:
    fill_queue(iterations)
    for thread_num in range(1, (concurrency + 1)):
        if work_queue.empty() is True:
            break
        worker = Thread(target=repeat)
        worker.start()
    work_queue.join()
