"""Project 1

#Rockaway Beach Scootershare Model

_A scootershare for Rockaway Beach in New York_

###By Joshua Sarceno, Osman Khan, Sebastian Zavala
"""

# install Pint if necessary

try:
    import pint
except ImportError:
    !pip install pint

# download modsim.py if necessary

from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)

download('https://raw.githubusercontent.com/AllenDowney/' +
         'ModSimPy/master/modsim.py')

# import functions from modsim

from modsim import *

"""#Movement of Scooters

The first code cell models the movement of scooters from one location to the other, with a shuttle being initiated if the number of scooters at a location is below a threshold.

"""

def scooter_to_beach(state,k1,d1,t1):
  """Move scooters from the lot to the beach.
  Initiate a transfer if the number of scooters is less than the threshold.

  d1=number of scooters moved from lot to the beach
  t1=threshold of the number of scooters at lot to initiate transfer.
  k1=the metric we are analyzing, number of scooters per transfer.
  """
  #By having a threshold, we will not have negative scooters at a location.
  if state.lot <=t1:
    state.beach -=k1
    state.lot +=k1
    state.shuttled_to_lot +=1
    state.number_of_shuttles +=1
    state.beach +=d1
    state.lot -=d1
    state.trips +=d1
    return
  state.beach +=d1
  state.lot -=d1
  state.trips +=d1

def scooter_to_lot(state,k1,d1,t1):
  """Move scooters from the beach to the lot.
  Initiate a transfer if the number of scooters is less than the threshold.

  d1=number of scooters moved beach lot to the lot
  t1=threshold of the number of scooters at beach to initiate transfer.
  k1=the metric we are analyzing, number of scooters per transfer.
  """
  #By having a threshold, we will not have negative scooters at a location.
  if state.beach <=t1:
    state.lot -=k1
    state.beach +=k1
    state.shuttled_to_beach +=1
    state.number_of_shuttles +=1
    state.lot +=d1
    state.beach -=d1
    state.trips +=d1
    return
  state.lot +=d1
  state.beach -=d1
  state.trips +=d1

"""#Nature of Time

The second code cell models a simulation of 6am-6pm. The day is divided into 720 minutes, with different flip probabilities for the three sections at each location.
"""

def run_simulation(state,k1,num_steps):
  """Have a specific probability at particular times at the two locations.
  k1=number of scooters per transfer
  num_steps=time of the day (a 12 hour period)
  """
  #num_steps*probability at each location is equal
  #1 step = 1 minute in time. 0 - 720 represents 6am-6pm.
  #customers who go to beach = customers to go to lot
  for i in range(0,120):
    if flip(0.55):
      scooter_to_beach(state,k1,d1,t1)
  for i in range(120,360):
    if flip(0.55):
      scooter_to_beach(state,k1,d1,t1)
    if flip(0.1):
      scooter_to_lot(state,k1,d1,t1)
  for i in range(360,600):
    if flip(0.1):
      scooter_to_beach(state,k1,d1,t1)
    if flip(0.55):
      scooter_to_lot(state,k1,d1,t1)
  for i in range(600,720):
    if flip(0.55):
      scooter_to_lot(state,k1,d1,t1)
  return state.number_of_shuttles

"""#Sweeping the Number of Scooters per Shuttle

The third code cell runs a sweep series over the number of scooters per transfer, represented by k1. The values it sweeps are 200-1,000, with a gap of 5 per consecutive values.
"""

"""Sweeps the values of k1 to see how many transfers are needed per day
"""
#d1=demand for scooters per minute
#t1=threshold to initiate a transfer of scooters
#color can be changed as desired
sweep = SweepSeries()
num_steps = 720
d1=90
t1=225
for k1 in range(200,1000,5):
    scootershare2=State(lot=2000,beach=0,shuttled_to_lot=0,shuttled_to_beach=0,number_of_shuttles=0,trips=0)
    sweep[k1]= run_simulation(scootershare2,k1,num_steps)
sweep.plot(label='total transfers to beach and lot', color ='purple')
decorate(title='Rockaway Beach Scootershare Model',
         xlabel='number of scooters per shuttle',
         ylabel='number of shuttle transfers per day')
print('unique customers:')
(scootershare2.trips)*.5

