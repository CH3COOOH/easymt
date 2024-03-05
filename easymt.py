import threading
import multiprocessing
import random

class EasyMT:
## emp = EasyMT()
## emp.addTask(func, func_name, (args..., ))
## emp.start(isWaitUntilFinish=False)
## emp.terminate_all()
	def __init__(self, multiX='process'):
		self.task_map = {}
		self.multiX = multiX
	
	def addTask(self, target, t_name, args=()):
		if self.multiX == 'process':
			self.task_map[t_name] = multiprocessing.Process(target=target, args=args)
		elif self.multiX == 'thread':
			self.task_map[t_name] = threading.Thread(target=target, args=args)
	
	def start(self, isWaitUntilFinish=True):
		for t_name in self.task_map.keys():
			print(f'Launch [{t_name}]...')
			self.task_map[t_name].start()
			
		if isWaitUntilFinish:
			for t_name in self.task_map.keys():
				self.task_map[t_name].join()
	
	def terminate(self, t_name):
		self.task_map[t_name].terminate()
		
	def terminate_all(self):
	## Work on multiprocessing
		for t_name in self.task_map.keys():
			self.task_map[t_name].terminate()

class qEasyMT:
	def __init__(self, multiX='process'):
		self.data_q = None
		self.emp = EasyMT(multiX)

	def __chunks(self, arr, m):
		from math import ceil
		n = int(ceil(len(arr) / float(m)))
		return [arr[i:i + n] for i in range(0, len(arr), n)]
	
	def addArray(self, d_arr):
		self.data_q = d_arr
	
	def start(self, n_tasks, func, const=None, isWaitUntilFinish=True, shuffle=False):
		if shuffle:
			random.shuffle(self.data_q)
		if len(self.data_q) < n_tasks:
			if const == None:
				func(self.data_q)
			else:
				func(self.data_q, const)
		else:
			data_distribute = self.__chunks(self.data_q, n_tasks)
			for i in range(n_tasks):
				if const == None:
					self.emp.addTask(func, f"qEMT_{i}", (data_distribute[i], ))
				else:
					self.emp.addTask(func, f"qEMT_{i}", (data_distribute[i], const, ))
			self.emp.start(isWaitUntilFinish)
		return 0

def test(a, b):
	import time
	while True:
		print('%d + %d = %d' % (a, b, a+b))
		time.sleep(3)

def test_pipe():
	import time
	def __task(arr):
		for i in arr:
			print(i)
			time.sleep(1)
	qemp = qEasyMT('thread')
	qemp.addArray([4,5,6,7,8,9,10,11,12,13])
	qemp.start(10, __task, shuffle=True)
	

if __name__ == '__main__':
	test_pipe()
	#import time
	#emp = EasyMT()
	#emp.addTask(test, "test1", (1, 2, ))
	#emp.addTask(test, "test2", (3, 4, ))
	#emp.addTask(test, "test3", (5, 6, ))
	#emp.start(isWaitUntilFinish=False)
	#time.sleep(10)
	#print('Bye~')
	#emp.terminate_all()