#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#
# @name:    Wascan - Web Application Scanner
# @repo:    https://github.com/m4ll0k/Wascan
# @author:  Momo Outaadi (M4ll0k)
# @license: See the file 'LICENSE.txt'

from os import path
from queue import Queue
from threading import Thread 
from lib.utils.check import *
from lib.utils.printer import *
from lib.utils.readfile import *
from lib.request.request import *
from lib.utils.settings import MAX

class adminpanel(Request):
	""" Potential Admin Panel """
	get = "GET"
	def __init__(self,kwargs,url,data):
		Request.__init__(self,kwargs)
		self.url = url 
		self.data = data

	def run(self):
		info('Bruteforce admin panel...')
		# set queue to MAX queues
		queue = Queue(MAX)
		for _ in range(MAX):
			# call ThreadBrute class
			thread = ThreadBrute(self.url,queue,self)
			# set daemon 
			thread.daemon = True
			# starting thread		
			thread.start()
		# reading file 
		for path in readfile(self.search()):
			queue.put(path.decode('utf-8'))
		queue.join()

	def search(self):
		""" search data path """
		realpath = path.join(path.realpath(__file__).split('plugins')[0],"lib/db/")
		return (realpath + "adminpanel.wascan")

class ThreadBrute(Thread):
	""" Bruteforcer """
	get = "GET"
	def __init__(self,target,queue,request):
		Thread.__init__(self)
		self.queue = queue
		self.target = target
		self.request = request

	def run(self):
		while True:
			try:
				#if self.queue.full() == False: exit()
				#if self.queue.empty() == True: exit()
				# check url path
				url = CPath(self.target,self.queue.get())
				# send request
				req = self.request.Send(url=url,method=self.get)
				# if status code == 200
				if req.code == 200:
					# and req.url == url
					if CEndUrl(req.url) == url:
						plus('A potential Admin Panel Page was found at: [%s] {}'.format(req.url) %(req.code))
				# done queue task
				self.queue.task_done()
			except Exception as e:
				pass
			except AttributeError as e:
				pass
			except TypeError as e:
				pass