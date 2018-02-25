
# Luis Leal (2018)





######################################################### travel_MAIN: USAGE and error messages


error_message3 = ' \n \
Error: latitude/longitude not in a recognizable format. \n \
Use the following format, for example: 59°19′46″N,18°4′7″E.  \n'






######################################################### libraries

import sys
import numpy as np
import time
from geopy.distance import vincenty		# used to compute linear distance between city pairs
from mpi4py import MPI                  # parallelization





######################################################### Auxiliary functions


##### Function used to convert coordinates from <Degrees Minutes Seconds> to <Decimal Degrees>

def geo_converter(location):
    try: 
        marker_deg = location.find('°')
        loc_deg = location[:marker_deg]
        location2 = location[(marker_deg + 1):]
        marker_minutes = location2.find('′')
        loc_min = location2[:marker_minutes]
        location3 = location2[(marker_minutes + 1):]  
        marker_seconds = location3.find('″')
        if marker_seconds != -1 :
            loc_sec = location3[:marker_seconds]
        else :
            loc_sec = 0
    except:
        print(error_message3) 
        exit() 

    dd = float(loc_deg) + float(loc_min)/60 + float(loc_sec)/3600

    if location.endswith('N') or location.endswith('E') :
        dd = dd
    elif location.endswith('S') or location.endswith('W') :
        dd = -dd
    else :
        print(error_message3) 
        exit() 

    return dd




#####  Function used to adjust itinerary based on start city defined by user

def adjust_itinerary(city_iteneray, city_list) :
    refcity_mark = np.where(city_iteneray == city_list[0])
    refcity_mark_aux = refcity_mark[0]

    # adjusted itinerary
    if refcity_mark_aux[0] != 0 :
        city_iteneray_adj = np.roll(city_iteneray, (len(city_iteneray)-refcity_mark_aux[0]))
    else :
        city_iteneray_adj = city_iteneray

    # create itinerary to be sent to standard output
    itinerary_out = ""
    for i in range(len(city_iteneray)):
        itinerary_out = itinerary_out + ' --> ' + city_iteneray_adj[i]
    itinerary_out = itinerary_out[5:] + ' --> ' + city_list[0]                 # '[5:]' removes initial arrow

    
    return city_iteneray_adj, itinerary_out






######################################################### MAIN MODULE


def gofaster(city_list, latitude_deg_list, longitude_deg_list, rank, size_MPI, comm) :


    ########  Convert coordinates from <Degrees Minutes Seconds> to <Decimal Degrees>

    latitude_decdeg_list = list()
    longitude_decdeg_list = list()

    for i in range(len(latitude_deg_list)):
        aux_lat = geo_converter(latitude_deg_list[i])
        latitude_decdeg_list.append(aux_lat)
        aux_lon = geo_converter(longitude_deg_list[i])
        longitude_decdeg_list.append(aux_lon)




    ######## Compute linear distance between city pairs using 'vincenty' from 'geopy.distance' library


    city_distances_dict = dict()

    for i in range(len(city_list)):
        for j in range(len(city_list)):
            city_1 = city_list[i]
            city_2 = city_list[j]
            if city_1 == city_2 : continue
            city_pair = city_1 + '_' + city_2
            city_1_coord = (latitude_decdeg_list[i], longitude_decdeg_list[i])
            city_2_coord = (latitude_decdeg_list[j], longitude_decdeg_list[j])
            #
            city_dist = vincenty(city_1_coord, city_2_coord).kilometers
            #
            city_distances_dict[city_pair] = city_dist





    ######## Find optimal itinerary

    import simann_optimize_cy3 as simann_opt

    #### Initial itineray (random)
    city_iteneray = np.copy(city_list)
    np.random.shuffle(city_iteneray)

    [city_iteneray_initial, itinerary_initial] = adjust_itinerary(city_iteneray, city_list)

    ## compute initial distance
    distance_ref = simann_opt.dist_itinerary(city_iteneray_initial,city_distances_dict)

    time.sleep(rank/4)
    print('\n Initial random itinerary (process', rank, '): \n', 'Distance (Km):', round(distance_ref,1), ' \n ITINERARY:', itinerary_initial, '\n')


    ## Compute optimal itinerary using simulated annealing optimization algorithm
    opt_solution = simann_opt.simann_control(city_iteneray_initial, city_distances_dict, distance_ref)

    ## Results
    # Optimised itinerary
    city_iteneray_best = opt_solution[0]

    # Optimal distance
    distance_best = opt_solution[1]



    ######## determine best MPI itinerary and send to standard output


    [city_iteneray_final, itinerary_f] = adjust_itinerary(city_iteneray_best, city_list)

    print('\n \n \n Optimised itinerary from process', rank, ': \n', 'Distance (Km):', round(distance_best,1), ' \n ITINERARY:', itinerary_f, '\n')


    #### Send output from each MPI process to 'rank 0' using comm.Reduce and determine best solution (min distance) >>> NOT IN USE

    # initializing variables. mpi4py requires that we pass numpy objects.
    #distance_best_rank = np.array(round(distance_best,1))
    #dist_MPI = np.zeros(1)

    # compare distances computed by different MPI processes, print minimum distance
    #comm.Reduce(distance_best_rank,dist_MPI, op=MPI.MIN, root = 0)
    #if comm.rank == 0: print('\n \n dist_MPI', dist_MPI, '\n')

    #if rank == 0 :
    #    # find best itenerary (compare distances computed by each MPI process, selected min)
    #    print()
    #    print('opt_solution_dist_MPI', opt_solution_dist_MPI, '\n')


 


    #### Send output from each MPI process to 'rank 0' using comm.Send & comm.Recv and determine best solution (min distance)  

    ## initializing variables
    data_MPI_dist = np.zeros(1)


    ## send/receive MPI data
    # distance
    if rank != 0: 
        data_MPI_dist[0] = round(distance_best,1)
        comm.Send(data_MPI_dist, dest=0, tag=10)                    #use tags to distinguish between different messages from the same sender 
    elif rank == 0 :
        opt_solution_dist_MPI = np.zeros(size_MPI)
        opt_solution_dist_MPI[0] = round(distance_best,1)
        for k in range(1,size_MPI):
            comm.Recv(data_MPI_dist, source=k, tag=10)
            opt_solution_dist_MPI[k] = data_MPI_dist[0]

    # itenerary
    if rank != 0: 
        comm.send(itinerary_f, tag=20, dest=0)
    elif rank == 0 :
        opt_solution_it_MPI = ['NaN'] * size_MPI
        opt_solution_it_MPI[0] = itinerary_f 
        #data_MPI_itinerary = tuple(data_MPI_itinerary)
        for k in range(1,size_MPI):
            aux_MPI_rec = list()
            aux_MPI_rec.append(comm.recv(tag=20, source=k))
            opt_solution_it_MPI[k] = aux_MPI_rec[0]

    # send best solution to standard output
    if rank == 0 :
        #
        # find best itenerary (compare distances computed by each MPI process, selected min)
        ind = np.unravel_index(np.argmin(opt_solution_dist_MPI, axis=None), opt_solution_dist_MPI.shape)
        print('\n \n BEST ITINERARY: \n Distance (Km):', opt_solution_dist_MPI[ind], ' \n ITINERARY:', opt_solution_it_MPI[ind[0]])

    
    if rank == 0:
        out_dist = opt_solution_dist_MPI[ind]
    else :
        out_dist = ""


    return out_dist





########################################################################################################################################


