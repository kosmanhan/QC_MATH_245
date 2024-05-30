"""Project 2

#Population and Votes

_Is the increase in Population and Election Votes of Israel from 1949 to 2021 related?_

###By Malka Danese & Osman Khan

##Initial Import & Download
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

#import functions from modsim, pandas, nupy, matplotlib.pyplot, and seaborn as sns, and run the code to have grids on all graphs
from modsim import *
from pandas import read_html
from numpy import linspace
from matplotlib.pyplot import plot
import seaborn as sns
sns.set_style('whitegrid')

"""##Glean Data from Web & Initilization

The first code cell gleans data from the 2 websites, takes 11th and 6th table for population and total votes respectively. The total votes data requires cleanup, i.e. renaming, and removing the first entry, which is an outlier. Both data sets are divided by one million.
"""

#download data from 2 html websites
download('https://en.wikipedia.org/wiki/Demographics_of_Israel')
download('https://en.wikipedia.org/wiki/Elections_in_Israel')

#named the website about Demographics filename1
filename1 ='Demographics_of_Israel'
tables = read_html(filename1,
                   header=0,
                   index_col=0,
                   decimal='M')
table_pop = tables[11]
#column of interest is named pop
pop=table_pop.Population/1e6

#named the website about Elections dataname
dataname = 'Elections_in_Israel'
tables = read_html(dataname,
                   header=0,
                   index_col=0,
                   decimal='.')
tableelections = tables[2]
#index is renamed into int, Apr 2019 and Sept 2019 are changed to 2018 & 2019
tableelections.index = [1949,1951,1955,1959,1961,1965,1969,1973,1977,1981,1984,1988,1992,1996,1999,2003,2006,2009,2013,2015,2018,2019,2020,2021,2022]
#column of interest is named votes
votes = tableelections.Totalvotes/1e6
#first entry is removed from column of interest and named newvotes
newvotes=votes[votes.index!=1949]

"""##Functions, Variables & Parameters for Population & Votes over Time

The second code cell defines variables, parameters, functions, system object, and plot functions. It also plots both population and total votes onto the same graph.

"""

'''
Create the necessary variables that will be required for further population simulation.
t_0=starting year
t_end=ending year
elapsed_time= total number of year
p_0=population at starting year
p_end=population at ending year
total_growth=total increase in population over the time period
annual_growth=average increase in population per year
'''

#system variables for population

t_0 = pop.index[1]
t_end=pop.index[-1]
elapsed_time=t_end-t_0
p_0=pop[t_0]
p_end=pop[t_end]
total_growth = p_end-p_0
annual_growth=total_growth/elapsed_time
#scaffolding: t_0, t_end, elapsed_time, p_0, p_end, total_growth, annual_growth

'''
Create the necessary variables that will be required for further total votes simulation.
te_0=starting election
te_end=ending election
elapsed_time_elections= total number of elections
v_0=total votes at starting election
v_end=total votes at ending election
total_growth_votes=total increase in total votes over the time period
annual_growth_in_votes=average increase in total votes per election
'''

#system variables for total votes
v_0=votes[1951]
v_end=votes[2021]
te_0=votes.index[1]
te_end=votes.index[-2]
total_growth_votes = v_end - v_0
elapsed_time_elections = te_end - te_0
annual_growth_in_votes = total_growth_votes/elapsed_time_elections
#scaffolding: te_0, te_end, elapsed_time_elections, v_0, v_end, total_growth_votes, annual_growth_in_votes


'''
Create a single system object which will include both population and total votes parameters
'''
#as population and total votes have different names, they are place in the same system object.
system = System(t_0=t_0,
               t_end=t_end,
               p_0=p_0,
               annual_growth=annual_growth,
               te_0=te_0,
               te_end=te_end,
               v_0=v_0,
               annual_growth_in_votes=annual_growth_in_votes)
#scaffolding: show(system)

'''
Create a plot function for population per year, and a plot function for total votes per election.
'''

def populationplot():
  pop.plot(style='.',color='orange',label='Total Population')
  decorate(xlabel='Year', ylabel='Total Number (in millions)')

def votes_counted():
  newvotes.plot(style='.',color='indigo',label='Total Votes')
  decorate(title='Population & Total Votes over Time',
           xlabel='Year',
           ylabel='Total Number (in millions)')
#plot both plot functions onto the same graph
populationplot()
votes_counted()

"""##Graphing LoBF for Increase in Population and Votes"""

'''
Create a LoBF for Population
t_array= the time period that was focused on, 1951-2021
'''
t_array=linspace(1951, 2021, 70)
#Because there was a jump in population in 1990 we decided to have two line functions to better represent the data
def line_func1(t):
    if t<1990:
        intercept = 1.4
        slope = .082
    else:
        intercept = -1.2
        slope = .149
    return intercept + slope*(t-1950)

'''
Create a run simulation that plots the LoBF for Population
'''
line_array3=TimeSeries()
for t in t_array:
  line_array3[t]=line_func1(t)


'''
Create a LoBF for Total Votes
te_electionarray = the elections that was focused on, 1950-2021
'''
te_electionarray = linspace(1950,2021,71)
#Because there was a jump in total votes in 1990 we decided to have two line functions to better represent the data
def electionmodel1growth1(te):
    if te<1990:
        intercept = .48
        slope = 0.047
    else:
        intercept = -.09
        slope = .063
    return intercept + slope*(te-1950)
'''
Create a run simulation that plots the LoBF for Total Votes
'''
line_arrayelection=TimeSeries()
for te in te_electionarray:
  line_arrayelection[te]=electionmodel1growth1(te)


#plotting population using line of best fit
line_array3.plot(style='-',color='green',label='line of best fit for population')
populationplot()
#plotting elections using line of best fit
line_arrayelection.plot(style='-',color='magenta',label='line of best fit for votes')
votes_counted()

"""##Net Growth and Net Growth Rate over Time and Population


"""

#net growth and net growth rate for population
netgrowth=-1*pop.diff(-1)
netgrowthrate=(netgrowth/pop)*100

#netgrowthrate for elections

#scaffolding: -1*newvotes.diff(-1)
votenetgrowth = -1*newvotes.diff(-1)
votenetgrowthrate = (votenetgrowth/votes)*100
#votenetgrowth
#votenetgrowthrate

#netgrowth over time
netgrowth.plot(style='.')
votenetgrowth.plot(style='.',label='Total Votes')
decorate(title='Net Growth over Time',xlabel='Year',ylabel='Net Growth (in millions)')

#netgrowthrate over time
netgrowthrate.plot(style='.',color='maroon')
votenetgrowthrate.plot(style='.',color='green',label='Total Votes')
decorate(title='Net Growth Rate over Time', xlabel='Year',ylabel='Net Growth Rate (in %)')

#netgrowth over population/votes
plot(pop,netgrowth,'.',color='grey')
plot(newvotes,votenetgrowth,'.',color='purple')
decorate(title='Net Growth over Population and Votes',xlabel='Population/Votes (in millions)',ylabel='Net Growth (in millions)')

#netgrowthrate over population/votes
plot(pop,netgrowthrate,'.',color='pink')
plot(votes,votenetgrowthrate,'.',color='black')
decorate(title='Net Growth Rate over Population and Votes',xlabel='Population/Votes (in millions)',ylabel='Net Growth Rate (in %)')

"""##Graphing Line of Best Fit for Net Growth Rate of Population and Votes over Time"""

#Line of Best Fit for Population
def line_func(t):
   intercept = 3
   slope = -0.018
   return intercept + slope*(t-1950)

line_array2=line_func(t_array)

#Line of Best Fit for Votes
def electionline_func2(te):
    intercept = 16
    slope = -0.18
    return intercept + slope *(te-1949)

electionline_array2 = electionline_func2(te_electionarray)

#plot net growth rate with line of best fit

netgrowthrate.plot(style='.',label='population net growth rate')
plot(t_array, line_array2, label='line of best fit for net growth rate of population',color='lime')
plot(te_electionarray,electionline_array2, label='line of best fit for net growth rate of votes',color='cyan')
votenetgrowthrate.plot(style='.',label='votes net growth rate')
decorate(title = 'Net Growth Rate over Time', xlabel='Year',ylabel='Net Growth Rate in %')

"""##Simulating Population and Total Votes Growth using LoBF of Net Growth Rate over Time as the Growth Function"""

def growth_func(t,pop,system):
  return line_func(t)/21

def egrowth_func(te,pop,system):
  return electionline_func2(te)/181

#run simulation for population

def run_simulation7(system,growth_func):
  results = TimeSeries()
  results[system.t_0] = system.p_0
  for t in range (system.t_0,system.t_end):
    growth = growth_func(t, results[t],system)
    results [t+1] = results[t] + growth

  return results

#run simulation for votes
def run_simulation8(system,egrowth_func):
  eresults = TimeSeries()
  eresults[system.te_0] = system.v_0
  for te in range (system.te_0,system.te_end):
    egrowth = egrowth_func(te, eresults[te],system)
    eresults [te+1] = eresults[te] + egrowth

  return eresults

#plot run simulations along with along population and votes

run_simulation7(system,growth_func).plot(label='Population Simulation',color='green')
populationplot()
run_simulation8(system,egrowth_func).plot(label='Voting Simulation')
votes_counted()
decorate(title ='Simulation Model')

