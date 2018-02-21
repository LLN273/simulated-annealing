

# Luis Leal (2018)





######################################################### libraries (general)

import numpy as np
cimport numpy as np




######################################################### Simulated annealing function


def simann_control(np.ndarray city_iteneray, dict city_distances_dict, double distance_ref) :

    cdef int n_cities
    cdef int step_counter

    cdef double temperature
    cdef double REFERENCE_TEMP
    cdef double COOLING_FACTOR
    cdef double distance_best
    cdef double distance_it
    cdef double dist_change

    cdef np.ndarray city_iteneray_best
    cdef np.ndarray new_iteneray


    ### simulated annealing

    # initialize variables
    temperature = 5E3
    REFERENCE_TEMP = 1E-3
    COOLING_FACTOR = 0.9999
    n_cities = len(city_iteneray)    
    distance_best = distance_ref
    city_iteneray_best = city_iteneray
    step_counter = 1
    
    while temperature > REFERENCE_TEMP :

        step_counter = step_counter + 1

        #permute two cities
        new_iteneray = np.copy(city_iteneray)
        city_exchange = np.random.choice(n_cities,2,replace=False)
        new_iteneray[city_exchange[0]] = city_iteneray[city_exchange[1]]
        new_iteneray[city_exchange[1]] = city_iteneray[city_exchange[0]]

        #new distance
        distance_it = dist_itinerary(new_iteneray,city_distances_dict)   

        #compare distances
        dist_change = distance_it - distance_ref

        #cost assessment
        if dist_change < 0 or np.exp(-dist_change/temperature) > np.random.uniform(0,1) :
            city_iteneray = np.copy(new_iteneray)
            distance_ref = distance_it
            if distance_it < distance_best :
                city_iteneray_best = np.copy(new_iteneray)
                distance_best = distance_it

        # decrease temperature
        temperature = temperature*COOLING_FACTOR
  

    return city_iteneray_best, distance_best







######################################################### Auxilaiary function (computes total distance associated to an itinerary)


def dist_itinerary(np.ndarray city_iteneray,dict city_distances_dict) :

    cdef int i
    cdef int aux_1 
    cdef double distance
    cdef double distance_2cities

    distance = 0
    for i in range(len(city_iteneray)-1) :
        distance_2cities = city_distances_dict.get((city_iteneray[i] + '_' + city_iteneray[i+1]), 0)
        distance = distance + distance_2cities

    distance_2cities = city_distances_dict.get((city_iteneray[len(city_iteneray)-1] + '_' + city_iteneray[0]), 0)
    distance = distance + distance_2cities
    
    return distance





