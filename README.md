# Projet_Bus_Sibra - A Python project using graphs

The Sibra Bus project is a set of classes and algorithms written in Python and used as practicals for a course on project management at the engineering school Polytech Annecy-Chambéry. The operation of the algorithm is quite basic: Find the shortest, the fastest or the foremost path between two bus stops in a network of bus lines. (For this project, two crossing lines were used as an example).

The project had to be self-made, and I managed to finish the milestones on time.

## Data structure

Choosing the right data structure to model this bus network was essential to simplify the design of my search algorithms. It was also necessary to take into account the type of schedule (weekdays or holidays).

## 3 Algorithms

I implemented an algorithm that calculates the shortest path between 2 bus stops depending on the type of the algorithm (see below)
In all cases, it was necessary to specify a departure date to take into account during the search (in order to take the next bus arriving at the departure stop, depending on the type of day).

* Shortest: the shortest, in number of arc
* Fastest: the fastest, but with potentially more arc
* Foremost: arrives at the earliest, no matter the arc numbers

In the example below the red line starts at 10:11, the green at 10:05 and the blue starts at 10:00. I want to leave around 10am. The green line responds to "Shortest", red to "Fastest" and blue to "Foremost".

![explanatory scheme](data/algorithms_explanations.PNG?raw=true "explanatory scheme")

## How to run it

Download the programm, and open sibra.py with a Python compiler. In this file, I wrote a few examples to run the different algorithms :

*shortest_way(planTest,"Chorus","CAMPUS")
*fastest_way(planTest,"GARE","LYCEE-DE-POISY","fastest",["22/03/19","6:00"])


A good example to see the difference between the Fastest and Foremost algorithms :
*fastest_way(planTest,"CAMPUS","GARE","foremost",["04/03/19","16:24"])
*fastest_way(planTest,"GARE","VIGNIERES","foremost",["23/03/19","9:26"])

