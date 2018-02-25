
# Travelfast 

Travelfast solves the traveling salesperson problem using the simulated annealing optimization algorithm. Travelfast is written in python/cython.
As simulated annealing is a greedy algorithm, the package is run using the MPI framework in order to increase the likelihood of
finding the best overall itinerary.


## Usage
```
mpiexec -n 16 travelfast.py inputfile.txt
```
Recommended number of parallel processes depends on the number of cities listed in the input file.
- For 4 cities, use 1 process (estimated runtime < 10 sec)
- For 10 cities, use 4 processes (estimated runtime < 20 sec)
- For 20 cities, use 16 processes (estimated runtime < 2 min)
- For 30 cities, use 64 processes (estimated runtime < 7 min)


## Input
File containing list of cities and respective latitude/longitude coordinates. The first city in the list is taken as the starting
point of the trip. There are four examples of input files included with the package, listing 4, 10, 20, and 30 cities, respectively.
(These four files are named 'city_list_X.txt', where 'X' is the number of cities).

Example of an input file (city_list_4.txt):
```
City,latitude,longitude
Stockholm,59°19′46″N,18°4′7″E
Gothenburg,57°42′N,11°58′E
Kiruna,67°51′N,20°13′E
Malmo,55°36′21″N,13°02′09″E
```

## Output
Best itinerary and associated distance are sent to standard output.

Example:
```
 BEST ITINERARY:
 Distance (Km): 2915.2
 ITINERARY: Stockholm --> Kiruna --> Gothenburg --> Malmo --> Stockholm

 Elapsed time: 5.6 sec
```

## Dependencies
gofaster.py: processes input data, calls optimization algorithm, and manages communications between MPI processes
simann_optimize_cy3: cythonized library that implements the simulated annealing optimization algorithm.





