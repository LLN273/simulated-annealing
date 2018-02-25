#!/usr/bin/env python3
""" Package solves the traveling salesperson problem using the simulated annealing optimization algorithm. """


# Luis Leal (2018)





######################################################### travel_MAIN: USAGE and error messages



error_message1 = ' \n \
USAGE: travel_MAIN <city_list.txt>\n \n \
where: \n \
city_list.txt     >> file containing list of cities and respective latitude/longitude coordinates  \n'


error_message2 = ' \n \
Error: input file either contains no data or data is not in a recognizable format. \n \
Use the following format: city,latitude,longitude.  \n'




######################################################### libraries

import sys
import numpy as np
import time
from geopy.distance import vincenty		# used to compute linear distance between city pairs
from mpi4py import MPI                  # parallelization







######################################################### Start timer
t0 = time.time()






######################################################### MPI initialization
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size_MPI = comm.Get_size()








######################################################### Import city list & geographic coordinates
######################################################### City list must include city name and latitude/longitude coordinates 


try: 
    inputfile_cities = open(sys.argv[1], 'r')             			
except:
    print('\n Error: input file missing.')
    print(error_message1) 
    exit() 



# read input file, get city names and coordinates

flag_header = 0

city_list = list()
latitude_deg_list = list()
longitude_deg_list = list()

for line in inputfile_cities:    
    if flag_header == 0 :
        flag_header = 1
        continue                   
    line = line.rstrip()
    try:
        city_marker = line.find(',')
        city = line[:city_marker]                       # get city name
        city_list.append(city)
        line2 = line[(city_marker+1):]
        lat_marker = line2.find(',')
        lat_deg = line2[:lat_marker] 					# get latitude
        latitude_deg_list.append(lat_deg)
        lon_deg = line2[(lat_marker+1):]                # get longitude
        longitude_deg_list.append(lon_deg)
    except:
        print(error_message2)
        exit() 

city_list = np.array(city_list)



######################################################### Compute best itenerary

import gofaster

gofaster.gofaster(city_list, latitude_deg_list, longitude_deg_list, rank, size_MPI, comm)

# print elapsed time
if rank == 0:
    print("\n Elapsed time:", round(time.time() - t0,1), 'sec \n')



########################################################################################################################################


