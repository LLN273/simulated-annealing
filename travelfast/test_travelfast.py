# test_travelfast.py
import gofaster
import pytest


@pytest.mark.parametrize("city_list,latitude,longitude, rank, size_MPI, comm, expected", [
    (['Stockholm', 'Gothenburg', 'Kiruna', 'Malmo'], ['59°19′46″N', '57°42′N', '67°51′N', '55°36′21″N'], ['18°4′7″E', '11°58′E', '20°13′E', '13°02′09″E'],0,1,'MPI.COMM_WORLD', 2915.2),
    (['Stockholm', 'Falun', 'Gothenburg', 'Kiruna', 'Lulea', 'Malmo', 'Trollhattan',
 'Umea', 'Uppsala', 'Orebro'], ['59°19′46″N', '60°36′26″N', '57°42′N', '67°51′N', '65°35′4″N', '55°36′21″N', '58°17′N', '63°49′30″N', '59°51′29″N', '59°16′26″N'],['18°4′7″E', '15°37′52″E', '11°58′E', '20°13′E', '22°9′14″E', '13°02′09″E', '12°17′E', '20°15′50″E', '17°38′41″E', '15°12′27″E']
,0,1,'MPI.COMM_WORLD', 3021)
])

def test_travelfast(city_list,latitude,longitude, rank, size_MPI, comm, expected):
    assert gofaster.gofaster(city_list, latitude, longitude, rank, size_MPI, comm) == expected






  
