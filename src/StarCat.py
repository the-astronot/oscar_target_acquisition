"""
________________
|_File_History_|________________________________________________________________
|_Programmer______|_Date_______|_Comments_______________________________________
| Max Marshall    | 2023-01-24 | Created File
|
|
|
"""


class Star:
	def __init__(self,ra,decl,Id,mag):
		self.id = int(Id)
		self.ra = ra
		self.decl = decl
		self.mag = mag

	def __str__(self):
		return "[STAR {0:04d}] -> [{1:.3f},{2:.3f},{3:.3f}]".format(self.id,self.ra,self.decl,self.mag)


class StarCat:
	def __init__(self, catalog):
		self.catalog = catalog
		self.stars = {}
		self.num_stars = 0
		self.deltaRA = 5
		self.deltaDecl = 5
		self.max_hash = int(self.get_hash(Star(360,-90,0,0)))
		self.generate_stars()
		print(self)

	def __str__(self):
		string = ""
		hashes = [x for x in range(0,self.max_hash)]
		for hash in hashes:
			ra = int(hash/(180/self.deltaDecl))
			de = int((hash%max(ra,1))-(90/self.deltaDecl))
			string += "QUADRANT {:05d} [({:03d},{:03d})->({:03d},{:03d})]:\n".format(hash,ra*self.deltaRA,de*self.deltaDecl,min((ra+1)*self.deltaRA,360),min((de+1)*self.deltaDecl,90))
			if hash in self.stars:
				for star in self.stars[hash]:
					string+=str(star)+"\n"
		string = string.strip("\n")
		return string

	def get_search_area(self, center, radius):
		tl = self.get_hash(Star(max(center[0]-radius,0),min(center[1]+radius,90),0,0))
		tr = self.get_hash(Star(min(center[0]+radius,360),min(center[1]+radius,90),0,0))
		bl = self.get_hash(Star(max(center[0]-radius,0),max(center[1]-radius,-90),0,0))
		br = self.get_hash(Star(min(center[0]+radius,360),max(center[1]-radius,-90),0,0))
		hashes = []
		print(bl,br,tl,tr)
		for i in range(bl,br+1,int(180/self.deltaDecl)):
			for j in range(1+tl-bl):
				hashes.append(i+j)
		return hashes

	def generate_stars(self):
		self.num_stars = 0
		with open(self.catalog,"rb") as f:
			while f.read(1).decode() != "":
				f.seek(-1,1)
				name = f.read(4).decode()
				f.seek(71,1)
				try:
					ra_h = int(f.read(2).decode())
					ra_min = int(f.read(2).decode())
					ra_sec = float(f.read(4).decode())
					de_sign = f.read(1).decode()
					de_sign = ((de_sign!="-")-0.5)*2
					de_deg = int(f.read(2).decode())
					de_min = int(f.read(2).decode())
					de_sec = int(f.read(2).decode())
					ra = hrminsec2deg(ra_h,ra_min,ra_sec)
					decl = de_sign*(de_deg+(de_min/60.0)+(de_sec/3600.0))
					f.seek(12,1)
					mag = float(f.read(4).decode())
					star = Star(ra,decl,name,mag)
					hash = self.get_hash(star)
					if hash in self.stars:
						self.stars[hash].append(star)
					else:
						self.stars[hash] = [star]
					self.num_stars += 1
				except ValueError:
					pass
				finally:
					newline = f.read(1).decode()
					while newline != "\n":
						newline = f.read(1).decode()

	def get_hash(self,star):
		# Find Bottom-Left value of encompassing grid
		ra_hash = int(star.ra/self.deltaRA)
		decl_hash = int((star.decl+90)/self.deltaDecl)
		return int(ra_hash*(180/self.deltaDecl) + decl_hash)



def hrminsec2deg(hr,minute,sec):
	return 15*hr + minute/(4.0) + sec/(240.0)


if __name__ == '__main__':
	test = StarCat("../data/bsc5.dat")
	hashes = test.get_search_area([354,67],1.0)
	print(hashes)