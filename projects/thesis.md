---
layout: project
type: project
published: true
image: images/13chip50.gif
title: Thesis
permalink: projects/thesis
date: 2018-10-12
labels:
  - Python
  - Parallel Programming
  - Simulation
  - HPC
  - MPI
  - C/C++
  
summary: "A Heuristic for Optimizing the Physical Layout and Network Topology of Integrated 3D Multi-chip Systems Under Temperature Constraints"
---

__Summary__

For my Master Thesis in computer science at the University of Hawaii at Manoa I
wrote a simulation to construct Integrated 3D Multi-chip systems.  Under the
guidance of my advisor Prof. [Henri Casanova](https://henricasanova.github.io/)
and in collaboration with Prof. [Michihiro
Koibuchi](https://www.nii.ac.jp/en/faculty/architecture/koibuchi_michihiro/) and
his KoiLab team I developed designs for single systems containing multiple
microprocessor chips.  The advantage of a single multi-chip system is high
computational power and low latency which is advantageous for running parallel
applications.  Common cluster architecture offer high computational power
however, microprocessor chips are not contained within one unit and a network is
required for communication.  The systems we design contain many microprocessor
chips in close proximity to one another in one system and they communicate via
either wired or unwired connections.  The inter-chip connections in our systems
offer a significantly greater bandwidth than those presented in common cluster
architecture such as Gigabit Ethernet or Infiniband.

<div class="ui images">
  <img class="ui image medium right floated round image" src="../images/13chip50.gif">
</div>

The challenges we had when constructing these systems is heat build up due to
chips in close proximity clocked at high frequencies.  Spacing out the chips is
a solution that leads to less heat build up but it leads to a sparser inter-chip
network which can be detrimental for communication.  Trade-offs exists and we
needed to build chip layouts that offer a good network, low operating
temperature, and high chip clock frequencies.  This is a multi-variate
optimization problem and we employed heuristics to help.  We utilize simulation
to implement our heuristics, generate heat profiles for constructed layouts, and
evaluate application performance on constructed layouts.

**Contributions**

The layout construction simulation was built using Python 2.7 and started by my
advisor.  I was tasked with completing the simulation code and implementing our
heuristic to generate the best layouts possible.  Our heuristic is based off a
greedy approach in which it evaluates the layouts and greedily chooses the
layouts with the best metrics(network, temperature, and power).  The simulator,
known as Hotspot,  which evaluates the layout temperature is slow and is the
bottleneck of our overall simulation.  

Significant effort went into the acceleration of Hotspot's runtime.  The Hotspot
code is written in C and thus we tried to use parallel programming tools and
techniques such as OpenMP and Message Passing Interface, MPI.  These attempts
led to little improvement in the runtime because Hotspot preforms a lengthy
large sparse, LU factorization.  Hotspot is called many times by our heuristic
in order to get temperature metrics.  We alleviated some of the bottle neck by
making parallel calls to Hotspot since we cannot speed Hotspot up directly.  We
first used the python multiprocessing modules but encountered errors when we
scaled up to run our simulation on many core machines.  We finally settled on
using MPI via the mpi4py module which helped with speed up of the overall
simulation runtime.

With access to two 32 core and one 16 core machines we were able to run our
heuristic simulation faster.  This opened up doors for me to implement other
features to improve the resulting layouts.  The rotating image/GIF is an example
of one of the layout designs we build with our heuristic and simulation.  The
black grids represent a square microprocessor chip and the red sections are
inter-chip connection points where high bandwidth communication happens.  This
layout is one of many and they all have good network characteristics, high
operating chip frequencies, and cool operating temperatures.   

__Learned__

This project allowed me to become comfortable and well versed in the Python
programming language.  During the course of my thesis, I learned to design and
simulate numerous experiments to gather data to build the best possible layouts.
I utilized remote machines and a Cray cluster to run simulations which helped me
to become more familiar with Linux/UNIX, ssh, and bash/shell scripting.  The
utilization of MPI helped me gain experience in developing, working with, and
debugging parallel code.  My concurrent and parallel programming skills greatly
improved during the course of my thesis.  My ability to write scientifically and
technically as well as present my findings were skills that I attribute to my
thesis work.  

*Copy of my thesis to be posted following defense

** Results from this work are up for publication.  Inquire via email for actual
results

<br/>
