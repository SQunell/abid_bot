# This code takes looks at the *.gp files and returns a file containg a list of the center of the black holes at each time
# files.txt is a list of all the times in the gp file this is generated by running something like
# ls | sed 's/h.t//' | sed 's/.ah1.gp//' | sort -n | sed '1,4d' > files.txt
# in the horizon directory (the last pipe removes other files that arent of the form h.t*.ah1.gp so that would be the thing to change)

from sys import argv
from os import listdir
from os.path import isfile, join
root_dir = argv[1]
iteration = int(argv[2])			# the iteration of the h5 files
time_step = float(argv[3])			# the code time step between each frame (This is calculated by looking at the file information after loading the h5 files in visit)
ahtype = argv[4]

all_dir = root_dir + "h5data/horizon/"
time_list = [ f[3:-7] for f in listdir(all_dir) if isfile(join(all_dir,f)) and f.find("h.t")  != -1  and f.find(".ah" + ahtype + ".gp") != -1]
time_list.sort(key=float)

out = open(root_dir + "bin/grid_code/bhcen" + ahtype + ".txt", 'w')

for ahtime in time_list:
	gp_file = open(all_dir + "h.t" + ahtime + ".ah" + ahtype + ".gp", 'r')
	origin_line = gp_file.readline()
	origin_line = gp_file.readline()
	coord_list = origin_line.split()

	t = str(float(ahtime)/float(iteration)*time_step)
	x = coord_list[3]
	y = coord_list[4]
	z = coord_list[5]
	
	out.write(t + "\t" + x + "\t" + y + "\t" + z + "\n")

	gp_file.close()

out.close()