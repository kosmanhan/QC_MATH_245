"""Project 3

#Simulation that Shows Alternative to the Stagnant Funding for Sex-Ed in America

_Can more federal funding for preventive STI measures reduce the percentage of population infected with chlamydia?_

###By: Tommaso Coraci, Malka Danese & Osman Khan

##Initial Import & Download
"""

# install Pint if necessary

try:
    from pint import UnitRegistry
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

download('https://github.com/AllenDowney/ModSimPy/raw/master/' +
         'modsim.py')

# import functions from modsim, pandas, nupy, matplotlib.pyplot, and seaborn as sns, and run the code to have grids on all graphs
from modsim import *
from pandas import read_html
from numpy import linspace
from matplotlib.pyplot import plot
from matplotlib import pyplot
import seaborn as sns
sns.set_style('whitegrid')
import pandas as pd

"""##Import & Glean Data From csv named Project3 and Plotting Line of Best Fit (LoBF)
Here, we import data regarding Chlamydia cases in the US from 1984-2020. We create lines of best fit that modeled the increase in cases. We plot both the cases and lines of best fit onto the same graph.

"""

df = pd.read_csv('Project3.csv')
df.index=df.Year
cols=["year", "rate", "percent"]
df.columns=cols

t_array=linspace(1984, 2019, 35) #2020 was an outlier
#Because PREP was founded in 2010 there was a drop in STDs, we decided to have two line functions to better represent the data
def line_func1(t):
    if t<2011:
        intercept = 9
        slope = 16.05
    else:
        intercept = 150
        slope = 10.9
    return intercept + slope*(t-1984)

line_array3=TimeSeries()
for t in t_array:
  line_array3[t]=line_func1(t)
#plotting data and line of best fit
df.rate.plot(style = '-', color = 'cyan', label = 'Number of Chlamydia cases')
line_array3.plot(style = '-',color='orange',label='Lines of Best Fit for the Population')
decorate(xlabel= 'Years',
         ylabel= 'Chlamydia cases per 100,000 people',
         title = 'The Growth of Chlamydia Cases from 1984-2019')

"""##Setting up SIM model
This is the code cell to set up the three different populations that are affected by the differential equations we created.
"""

#numbers chosen for population proportion came from research
def make_system(beta, gamma, theta):
    init = State(S=310, I=6, M=0.1) #in terms of millions
    init /= init.sum()

    return System(init=init, t_end=365, t_0=0,
                  beta=beta, gamma=gamma, theta=theta,tc=tc,tm=tm,tr=tr)

#this will create a state function with three different but connected and related populations.
def update_func(t, state, system):
    s, i, m= state

    treated = system.theta *m
    infected = system.beta *i *s
    medicated = system.gamma *i

    s += treated - infected
    i += infected -medicated
    m += medicated -treated

    return State(S=s, I=i, M=m,)

#the three time in days values were assumptions based on research

tc = 3             # time between contacts in days
tm = 7             # treatment time in days
tr = 7             # return to susceptibility in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tm     # treatment rate in per day
theta = 1 / tr     # return to susceptibility rate in per day

#this runs the simulation through a frame, using the three populations and systems.
def run_simulation(system, update_func):
    frame = TimeFrame(columns=system.init.index)
    frame.loc[0] = system.init
    for t in range(0, system.t_end):
        frame.loc[t+1] = update_func(t, frame.loc[t], system)
    return frame

#this plots the simulation, showing the three populations at the same time.
def plot_sim(r):
  r.plot(xlabel='number of days simulation is run for',ylabel='% of population',title="SIM Model with initial populations")

system=make_system(beta,gamma,theta)
results=run_simulation(system, update_func)
plot_sim(results)

"""##Finding a Realistic Value for Beta
This code cell was used to find the Beta value that corresponded to the U.S. population.
"""

#this sweeps the beta value over the SIM, using the max % of population infected as the metric.
def sweep_beta(beta_array,gamma,theta):
  sweep = SweepSeries()
  for beta in beta_array:
    system=make_system(beta,gamma,theta)
    results=run_simulation(system,update_func)
    sweep[beta] = results.I.max()
  return  sweep

beta_array=linspace(0.05,4,80)
#beta_array=linspace(0.05,0.25,20)
infected_sweep = sweep_beta(beta_array,gamma,theta)
infected_sweep.plot(xlabel='beta value',ylabel='max % of population infected',title='Effect of beta value on % infected')

"""##Interventions"""

'''
We are seeing the effect of funding on the percentage of population infected
The change in beta values based on funding were assumptions
fraction1=2/3 #no funding
fraction2=4/3 #increase of 25 million
fraction3=5/3 #increase of 50 million
fraction4=2 #increase of 75 million
fraction5=7/3 #increase of 100 million
'''
#we create three empty lists for beta values, systems, and results of those system on which SIM is run
fractionlist=[]
systemlist=[]
resultslist=[]
#this populates the three lists with beta values as the intervention, and prepares for the simulation based on the beta values.
for i in range(7):
  fractionlist.append((i+2)/3)
  systemlist.append(i)
  resultslist.append(i)

#this defines the intervention as a change in contact rate and beta value.
def add_funding(system, fraction):
    system.tc = system.tc*fraction
    system.beta=1/system.tc

#this runs the simulation over different system objects based on the intervention specified beta value.
for i in range(7):
  systemlist[i] = make_system(beta,gamma,theta)
  add_funding(systemlist[i],fractionlist[i])
  resultslist[i] = run_simulation(systemlist[i], update_func)
#scafolding, this will plot each sim model individually


#this defines a function that plots different interventions onto the same graph.
def plot_s(o,p,q,r,s,t):
  o.plot(label="1/2")
  p.plot(label="1/3")
  q.plot(label="1/4")
  r.plot(label="1/5")
  s.plot(label="1/6")
  t.plot(color='teal',label="1/7")
  decorate(title = 'Effect on Different Interventions on % of Population Infected',
           xlabel='Number of Days Simulation is run for',ylabel='% of population that is Susceptible',)

#we plot all interventions on the same graph
plot_s(resultslist[0].S,resultslist[1].S,resultslist[2].S,resultslist[3].S,resultslist[4].S,resultslist[5].S)
pyplot.legend(loc="upper right",title="Beta Values")

#this plots all intervention affected simulations separetely,
#while also showing the proportion of the three different populations.
for i in range(7):
  plot_sim(resultslist[i])

