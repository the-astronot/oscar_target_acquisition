"""
________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2023-01-24 | Created File
|
|
|
"""
import matplotlib.pyplot as plt
import math
import numpy as np
import Body
import random


class Simulation:
	def __init__(self, deltaT):
		self.t_step = deltaT
		self.satellites = []
		self.body = Body.Earth()
		self.satellites.append(Body.Oscar([3500,6805,2200],[-7.511,0.357,4.447]))

	
	def advance(self):
		for sat in self.satellites:
			a = self.calc_acceleration(sat)
			sat.move(self.t_step,a)

	def calc_acceleration(self, satellite):
		# 2 Body Motion around self.body
		try:
			r = np.subtract(satellite.p,self.body.p)
			abs_r = math.sqrt(r[0]**2+r[1]**2+r[2]**2)
			return -1*self.body.mu*(r/(abs_r**3))
		except ValueError:
			return None

	
	def plot(self):
		fig = plt.figure()
		ax = fig.add_subplot(projection="3d")
		bx,by,bz = self.body.plot()
		ax.scatter(bx,by,bz,c="b",s=0.1)
		for i in range(len(self.satellites)):
			sx,sy,sz = self.satellites[i].plot()
			ax.scatter(sx,sy,sz)
			[cx,cy,cz], _, _ = self.satellites[i].dir_of_travel()
			ax.plot([sx,sx+cx],[sy,sy+cy],[sz,sz+cz])
		ax.set_box_aspect([1,1,1])
		plt.show()


if __name__ == '__main__':
	test = Simulation(random.uniform(100,400))
	test.plot()
	while True:
		test.advance()
		test.plot()
		stars = test.satellites[0].get_stars()
		test.satellites[0].get_view(stars)
