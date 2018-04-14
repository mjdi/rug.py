#! python
import sys, getopt, math

# Written by Marcus Diemand on April 4th 2018 to solve standupmath's "The Rug Puzzle" open problem
# https://www.youtube.com/watch?v=HViA6N3VeHw
# using a square grid coordinate system (exploiting the slopes of lines being unity, 0, or infinity)
# and brute-forcing every uniquely constructed triangle confined to the tessellated rug in the video

# Imgur link to screenshot of answers to example puzzle (5 x 2, verbose)and to main puzzle (20 x 18): 
# https://i.imgur.com/ZM0HiXs.png
# takes approximately 4.5 minutes to run the (20x18) case on a ThinkPad T430s (3rd gen Ivy Bridge i5)

class Point(object):
as
	def setIsKiteCenter(self):
		self.isKiteCenter = True
	
	def getX(self):
		return self.X
		
	def getY(self):
		return self.Y
		
	def getIsKiteCenter(self):
		return self.isKiteCenter
		
	def __eq__(self, other):
		return self.__dict__ == other.__dict__
		
	def label(self):
		return "(" + str(self.X) + "," + str(self.Y) + "), isKiteCenter = " + str(self.isKiteCenter)

		
def main(argv):
	# get command line options
	try:
		opts, args = getopt.getopt(argv,"hvc:r:", ["col=","row="])
	except getopt.GetoptError:
		print("rug.py -c <number of columns> -r <number of rows>")
		sys.exit(2)
	
	# when True prints 3 points' coordinates and if they're each a "kite center" for each unique triangle
	# be quite careful with this verbose option when dealing with exceedingly large values of c & r !!!)
	# use Ctrl+C to stop the run time on the command line if necessary
	verbose = False
	
	# hardcode the example provided at 1:26 in https://www.youtube.com/watch?v=HViA6N3VeHw&t=1m26s
	c = 5
	r = 2
	
	# handle command line options
	for opt, arg in opts:
		if opt == "-h":
			print("rug_brute_force.py -c <number of columns> -r <number of rows>")
			sys.exit()
		elif opt == "-v":
			verbose = True
		elif opt in ("-c", "--col"):
			c = int(arg)
		elif opt in ("-r", "--row"):
			r = int(arg)
	
	# empty array of all points for defining all points on tesselated rug
	a=[]

	# add one to both c & r to yield number of vertical and horizontal lines demarcating square grid
	vert = c+1
	horz = r+1
	
	# generate all the points comprising a square grid from (1,1) to (vert,horz)
	for x in range (1, vert+1):
		for y in range (1, horz+1):
			p = Point(x,y)
			
			# identify "kite center" points which checker across the tessellated rug (hence modulus)
			if ((x-1) % 2 == 1 and (y-1) % 2 == 0) or ((x-1) % 2 == 0 and (y-1) % 2 == 1): 
				p.setIsKiteCenter()
				
			a.append(p)
	
	# empty dictionary/hash for all unique sets of three points, i.e.
	# only 1 unique triangle per the 6 permutations of 3 points
	d={}

	for p1 in a:
		for p2 in a:
			for p3 in a:
			
				# first assume not a valid triangle
				isTriangle = False
				num_diag = ""
			
				# we need three different points to make a triangle
				if p1.__eq__(p2) or p1.__eq__(p3) or p2.__eq__(p3):
					continue
				else:
				
					# calculate the 3 slopes found between all 3 pairs of points, 
					# accounting for infinite slope (div by 0) with try catch (redefine as -1)
					try:
						s_p1p2 = math.fabs( (p1.getY() - p2.getY()) / (p1.getX() - p2.getX()) )
					except:
						s_p1p2 = -1
					try:
						s_p1p3 = math.fabs( (p1.getY() - p3.getY()) / (p1.getX() - p3.getX()) )
					except:
						s_p1p3 = -1						
					try:
						s_p2p3 = math.fabs( (p2.getY() - p3.getY()) / (p2.getX() - p3.getX()) )
					except:
						s_p2p3 = -1						
					
					# need at least one 45 degree angle (slope 1 or -1) for a triangle
					if s_p1p2 == 1 or s_p1p3 == 1 or s_p2p3 == 1:
					
						# either a one-diagonal 45 deg isosceles triangle:
						if ((s_p1p2 == 1) + (s_p1p3 == 1) + (s_p2p3 == 1)) == 1:
						
							# disallow kite centers from making triangles with each other 
							if ((p1.getIsKiteCenter() == 1) + (p2.getIsKiteCenter() == 1) + (p3.getIsKiteCenter() == 1)) < 2: 
								
								# ensure the other two slopes are infinity and 0
								s_p1p2_slope_check = (s_p1p2 == 1 and ( (s_p1p3 == 0 and s_p2p3 == -1) or (s_p1p3 == -1 and s_p2p3 == 0) ) )
								s_p1p3_slope_check = (s_p1p3 == 1 and ( (s_p1p2 == 0 and s_p2p3 == -1) or (s_p1p2 == -1 and s_p2p3 == 0) ) )
								s_p2p3_slope_check = (s_p2p3 == 1 and ( (s_p1p2 == 0 and s_p1p3 == -1) or (s_p1p2 == -1 and s_p1p3 == 0) ) )
								
								if s_p1p2_slope_check or s_p1p3_slope_check or s_p2p3_slope_check: 
									isTriangle = True
									num_diag = "one-diag"
									
						# or a two-diagonal 45 deg isosceles triangle:
						elif ((s_p1p2 == 1) + (s_p1p3 == 1) + (s_p2p3 == 1)) == 2:
						
							# must not be made of any kite center points
							if ((p1.getIsKiteCenter() == 1) + (p2.getIsKiteCenter() == 1) + (p3.getIsKiteCenter() == 1)) == 0: 
							
								# ensure the last slope is infinity or 0
								s_p1p2_slope_check = ((s_p1p2 == 0 or s_p1p2 == -1) and s_p1p3 == 1 and s_p2p3 == 1)
								s_p1p3_slope_check = ((s_p1p3 == 0 or s_p1p3 == -1) and s_p1p2 == 1 and s_p2p3 == 1)
								s_p2p3_slope_check = ((s_p2p3 == 0 or s_p2p3 == -1) and s_p1p2 == 1 and s_p1p3 == 1)
								
								if s_p1p2_slope_check or s_p1p3_slope_check or s_p2p3_slope_check:
									isTriangle = True
									num_diag = "two-diag"
				
					# if it's found to be a valid triangle on the tessellated rug, try to record it
					if isTriangle:
					
						# avoid repeated dict/hash key permutations!!!
						
						t_permute = ["triangle: " + p1.label() + ";\t" + p2.label() + ";\t" + p3.label(),
									 "triangle: " + p1.label() + ";\t" + p3.label() + ";\t" + p2.label(),
									 "triangle: " + p2.label() + ";\t" + p1.label() + ";\t" + p3.label(),
									 "triangle: " + p2.label() + ";\t" + p3.label() + ";\t" + p1.label(),
									 "triangle: " + p3.label() + ";\t" + p1.label() + ";\t" + p2.label(),
									 "triangle: " + p3.label() + ";\t" + p2.label() + ";\t" + p1.label()]
									 
						repeat = False
						
						for t in t_permute:
						
							if t in d.keys():
								repeat = True
								
						if repeat == False:
							d[t] = t
							
							if verbose:
								print(num_diag + " " + t)
	
	# print a concluding statement containing the brute-force calculated answer for the given inputs
	print("There are " + str(len(d)) + " unique triangles for a tessellated rug with " + 
							 str(c) + " columns and " + str(r) + " rows!!!")
		
if __name__ == "__main__":
   main(sys.argv[1:])
