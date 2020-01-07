---
layout: project
type: project
published: True
image: images/projects/written_digit.gif
title: Digit Recognition From Wrist Movements and Security Concerns with Smart Wrist Wearable IOT Devices
permalink: projects/handwriting_hicss
date: 2019
labels:
  - Artificial Intelligence
  - A.I.
  - Machine Learning
  - Cyber Security
  - Wearable IOT
  - Python
  - Arduino
  - HICSS
  - Publication

summary: Built a machine learning model to identify digits being written users who are wearing smart wrist devices.

---
Manuscript found at [Digit Recognition From Wrist Movements and Security
Concerns with Smart Wrist Wearable IOT Devices](http://hdl.handle.net/10125/64532).

[Abstract found HERE](../project_extra/hicss_abstract)

__Summary__

In this project we explore topics in three big areas in computer science which
includes machine learning, cyber security, and wearable Internet of things
(IOT).  Wrist wearable IOT devices such as the Apple watch, Fitbit, and Samsung
watches are growing in popularity and becoming more common.  Wrist wearable IOT
devices most often come equipped with an accelerometer and a gyroscope hardware.  Many
algorithm, machine learning derived and not, utilize the data from these
hardwares to perform task recognition.  For instance, wrist wearable IOT can
detect when users are running, walking, sleeping, etc.  In this project we explore the
hypothesis that wearable IOT hardware can recognize fine motor task, such as
handwriting digits.

<div class="ui images">
  <div class="ui large black ribbon label">
	Prototype of our data collection device mounted on a participants wrist
  </div>
  <img class="rotate180 ui image large center floated round image"
src="../images/projects/hand_write_proto.jpg">
</div>

<!--div class="field">
  <div class="ui pointing red basic label">
	Prototype of our data collection device mounted on a participants wrist
  </div>
</div-->

We built a custom device equipped with an accelerometer and a gyroscope to
collect the data.  The hardware components fall under the Arduino family and
thus we wrote the hardware code using Arduino's IDE.  Volunteers were recruited
to wear our device and write the digit zero or the digit one while we recorded
the data from the accelerometer and gyroscope.  Python was used to parse, clean,
and process the hardware data.  The cleaned data was then used to build a
machine learning model that can classify the data coming from our device as the
digit zero or the digit one.  In other words, our machine learning model was
able to identify the digit a user was writing based off the subtle movements of
the wrist during writing.  A further exploration of our model, data, and
methodology is detailed in our manuscript.  Our findings lead us to investigate
potential security implications of our machine learning model.  A simple was
model was used yet it had excellent accuracy.  While we only focused on two
digits, our findings do not lead us to believe that classifying all digit, 0-9,
would be a more difficult task by comparison.  Additionally, more complex and
powerful models exists to handle harder problems.  Extrapolating form our work
and findings could imply that powerful machine learning models can identify
numbers user are writing and this is a security concern. Valuable and sensitive
information is often times in the form of numbers such as, credit card, PIN,
and social security numbers.


**Contributions**

My background in computer science made me the perfect person to handle the
programming, software, and machine learning components of the project.  I was
tasked with programming the hardware, in Arduino, to capture the necessary info
from the hardware on our device.  Using Python, I was able to clean, process,
and organize the data.  Before choosing what type of machine learning model I
wanted to use I had to gain a better understanding and intuition of the
collected data.  I performed a PCA analysis to identify which components
contained the most variability.  Several visualizations were also generated to
help us better understand how to build a good machine learning classifier.  I
ultimately built the machine learning model using extreme gradient boosting
and used an exhaustive grid search to optimize the hyper-parameters. 

__Learned__

The Arduino and hardware component was an extremely eye opening portion of this
project.  As someone with a computer science background, I am use to building
software and am often abstracted away form the hardware that runs our software.
During this project I was intimately involved in the hardware and I learned how
to write efficient code for embedded hardware for which speed was important.  

This project was also an exercise in machine learning.  In my current
[job](../work/uhcc) I have assumed more of a data
scientist role rather than a software developer role. Machine learning has
become an important part of what I do for work.  This project allowed me to
practice and hone my machine learning skills.  I gained further experience in
data preprocessing, model building, model tuning, and cross validation.

The finding from this project were written up into a formal manuscript and was
accepted by [Hawaii International Conference on Science Systems
(HICSS)](https://hicss.hawaii.edu) for their 2020 proceedings.  
<!--The manuscript
writing and review process was also a learning experience that is detailed
[HERE](../essays/my_first_paper).-->

<br>
