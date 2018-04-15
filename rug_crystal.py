#! python
import sys, getopt, math

# Written by Marcus Diemand on April 15th 2018 to solve standupmaths' "The Rug Puzzle" open problem
# https://www.youtube.com/watch?v=HViA6N3VeHw

class Point(object):

	def __init__(self, X, Y, vert, horz):
		self.X = X
		self.Y = Y
		self.vert = vert
		self.horz = horz
		# initially assume point is a kite edge vs. a kite center
		self.isKC = False

	def setXY(self, X, Y):
		self.X = X
		self.Y = Y

	def onRug(self):
		if self.X >= 1 and self.X <= self.vert and self.Y >= 1 and self.Y <= self.horz:
			return True
		else:
			return False
		
	def setIsKC(self):
		self.isKC = True
		
def main(argv):
	# get command line options
	try:
		opts, args = getopt.getopt(argv,"hvc:r:k:", ["col=","row=","kc="])
	except getopt.GetoptError:
		print("rug.py -h <help> -v <verbose> -c <number of columns> -r <number of rows> -k <1 if kitecenter at (1,1), 0 otherwise>")
		sys.exit(2)
	
	# hardcode the example provided at 1:26 in https://www.youtube.com/watch?v=HViA6N3VeHw&t=1m26s
	v = 0
	c = 5
	r = 2
	k = 0
	
	# handle command line options
	for opt, arg in opts:
		if opt == "-h":
			print("rug.py -h <help> -v <verbose> -c <number of columns> -r <number of rows> -k <1 if kitecenter at (1,1), 0 otherwise>")
			sys.exit()
		elif opt == "-v":
			v = 1
		elif opt in ("-c", "--col"):
			c = int(arg)
		elif opt in ("-r", "--row"):
			r = int(arg)
		elif opt in ("-k", "--kc"):
			k = int(arg)
	
	# empty array of all points for defining all points on tessellated rug
	a=[]
	# add one to both c & r to yield number of vertical and horizontal lines demarcating square grid
	vert = c+1
	horz = r+1
	
	# generate all the points comprising a square grid from (1,1) to (vert,horz)
	for x in range (1, vert+1):
		for y in range (1, horz+1):
			p = Point(x,y,vert,horz)
			
			# identify "kite center" points which checker across the tessellated rug (hence modulus)
			if k == 0:
				if ((x-1) % 2 == 1 and (y-1) % 2 == 0) or ((x-1) % 2 == 0 and (y-1) % 2 == 1): 
					p.setIsKC()
			elif k == 1:
				if (math.fabs(x-y) % 2 == 0): 
					p.setIsKC()
				
			a.append(p)

	# counter for number of triangles found
	n = 0
	# define the two "tracers" for the 8 possible crystals propagating from each right angle
	t1 = Point(1,1,vert,horz)
	t2 = Point(1,1,vert,horz)
 	# set of vectors defining the growth of the 8 crystals in the t1 and t2 directions
 	# cardinal directions between the two arms of the right angle: NW, SW, SE, NE, S, E, N, W
	t18 = [[-2, 0], [-2, 0], [2, 0], [2,0], [-1,-1], [1, 1], [-1,1], [-1,-1]]
	t28 = [[ 0, 2], [0, -2], [0,-2], [0,2], [ 1,-1], [1,-1], [ 1,1], [-1, 1]]

	for p in a:
		for i in range(0,8):
			# set each tracer's location to that of the current right angle point
			t1.setXY(p.X,p.Y)
			t2.setXY(p.X,p.Y)

			if i >= 4 and p.isKC:
				continue
			elif i < 4 and p.isKC:
				t1.setXY(t1.X + int(1/2*t18[i][0]), t1.Y + int(1/2*t18[i][1]))
				t2.setXY(t2.X + int(1/2*t28[i][0]), t2.Y + int(1/2*t28[i][1]))
			else:
				t1.setXY(t1.X + t18[i][0], t1.Y + t18[i][1])
				t2.setXY(t2.X + t28[i][0], t2.Y + t28[i][1]) 

			while t1.onRug() and t2.onRug():
				# print out triangles (comprising right angle point and two tracer points) if v is set to 1, i.e. "verbose mode"
				if v == 1:
					print("New triangle:\tpKC=" + str(p.isKC)[0] +
						"\t[" + str(t18[i][0]) + "," + str(t18[i][1]) +
						"]\t[" + str(t28[i][0]) + "," + str(t28[i][1]) + 
						"]\t(" + str(p.X)  + "," + str(p.Y)  + 
					   	")\t(" + str(t1.X) + "," + str(t1.Y) + 
					   	")\t(" + str(t2.X) + "," + str(t2.Y) + ")")

				n = n + 1
				t1.setXY(t1.X + t18[i][0], t1.Y + t18[i][1])
				t2.setXY(t2.X + t28[i][0], t2.Y + t28[i][1])
				
	if k == 1:
		print("Found " + str(n) + " unique triangles for a tessellated rug with " + 
							 str(c) + " columns, " + str(r) + " rows, and a kite center at (1,1)")
	elif k == 0:
		print("Found " + str(n) + " unique triangles for a tessellated rug with " + 
							 str(c) + " columns, " + str(r) + " rows, and no kite center at (1,1).")
		
if __name__ == "__main__":
   main(sys.argv[1:])
