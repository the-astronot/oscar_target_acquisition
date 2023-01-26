"""
________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2023-01-25 | Created File
|
|
|
"""
import math
import random
import numpy as np
import StarCat as SC
import Camera


class Body:
	def __init__(self, name, r, v, theta):
		self.name = name
		self.p = np.asarray(r)
		self.dp = np.asarray(v)
		self.theta = theta
		self.hash = random.getrandbits(32)

	def __eq__(self, object):
		return self.hash == object.hash

	def move(self, t, a=None):
		if a is not None:
			self.dp = np.add(self.dp,a*t)
		self.p = np.add(self.p,self.dp*t)

	def plot(self):
		return self.p[0],self.p[1],self.p[2]


class Earth(Body):
	def __init__(self):
		super().__init__("Earth", [0,0,0],[0,0,0],[0,0,0])
		self.radius = 6378 # km
		self.mu = 398600 # km^2/s^3

	def plot(self):
		num_subd = 50
		twopir = 2*math.pi
		x = []
		y = []
		z = []
		for a in range(num_subd):
			for b in range(num_subd):
				i = a/float(num_subd) * twopir
				j = b/float(num_subd) * twopir
				x.append(self.radius*math.cos(i)*math.cos(j))
				y.append(self.radius*math.sin(i)*math.cos(j))
				z.append(self.radius*math.sin(j))
		return x,y,z
	

class Oscar(Body):
	def __init__(self, r, v):
		super().__init__("Oscar",r,v,[0,0,0])
		self.camera = Camera.Camera(1080,1080,2/1080.,2/1080.,4)
		self.starcat = SC.StarCat("../data/bsc5.dat")
		self.fov = 2

	def dir_of_travel(self):
		v = math.sqrt(self.dp[0]**2 + self.dp[1]**2 + self.dp[2]**2)
		direction = self.dp/v
		print(direction)
		decl = math.asin(direction[2])
		ra = math.acos((direction[0]/math.cos((decl))))
		decl = math.degrees(decl)
		ra = math.degrees(ra)
		print(ra,decl)
		self.ra = ra
		self.de = decl
		return direction, ra,decl

	def get_stars(self):
		_, ra, de = self.dir_of_travel()
		hashes = self.starcat.get_search_area([ra,de],self.fov)
		stars = []
		for hash in hashes:
			if hash in self.starcat.stars:
				for star in self.starcat.stars[hash]:
					stars.append(star)
		return stars

	def get_view(self, stars):
		self.camera.generate_view(stars,self.ra,self.de)


if __name__ == '__main__':
	test = Body("test",[15000,12000,9000],[2,4,7],[0,0,0])
