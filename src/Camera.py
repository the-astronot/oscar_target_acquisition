"""
________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2023-01-26 | Created File
|
|
|
"""
from PIL import Image, ImageFilter
import math
import numpy as np


class Camera:
	def __init__(self, u, v, dpu, dpv, mag_max):
		self.u = u
		self.v = v
		self.dpu = dpu
		self.dpv = dpv
		self.mag_max = mag_max
		self.fov = [u*self.dpu,v*self.dpv]
		aspect_ratio = v/float(u)
		canv = 4000
		self.infsize = (canv,int(canv*aspect_ratio))
		self.view = Image.new(mode="L",size=(u,v))


	def generate_view(self, stars, ra, de):
		print(self.infsize)
		print(self.fov)
		self.infinity = Image.new(mode="L",size=self.infsize)
		dpuinf = self.fov[0]/float(self.infsize[0])
		dpvinf = self.fov[1]/float(self.infsize[1])
		print(dpuinf)
		print(dpvinf)
		# Add Background noise
		for star in stars:
			weight = int(min(255/(2.512**(star.mag-self.mag_max)),255))
			dra = star.ra - (ra-self.fov[0]/2.0)
			dde = star.decl - (de-self.fov[1]/2.0)
			center = (int(dra/dpuinf),int(dde/dpvinf))
			duinf = int(star.radius/dpuinf)
			dvinf = int(star.radius/dpvinf)
			if 0<center[0]<self.infsize[0] and 0<center[1]<self.infsize[1]:
				for i in range(0,duinf):
					for j in range(0,dvinf):
						if i == j == 0:
							u,v = center
							print("PUT PIXEL",u,v,weight)
							self.infinity.putpixel((u,v),weight)
						elif math.sqrt(((i*dpuinf)**2)+((j*dpvinf)**2)) < star.radius:
							for k in range(4):
								a = int((int(k/2)-0.5)*2)
								b = int(((k%2)-0.5)*2)
								u = center[0] + a*i
								v = center[1] + b*j
								if 0<u<self.infsize[0]:
									if 0<v<self.infsize[1]:
										print("PUT PIXEL",u,v,weight)
										self.infinity.putpixel((u,v),weight)
		#self.infinity = self.infinity.filter(ImageFilter.GaussianBlur(10))
		self.infinity.show()


if __name__ == '__main__':
	test = Camera(1080,1080,1/1080.,1/1080.,3.4)
