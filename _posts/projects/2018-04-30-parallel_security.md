---
layout: post
cover: assets/images/projects/stega.png
title: Parallel Steganographic Encryption
date: 2018-04-30
categories: projects
author: Lambert
featured: false
permalink: projects/parallel_steganographic_encryption
comments: true
labels:
 
  - Security
  - Steganography
  - Encryption 
  - OpenCV
  - C/C++
  - Parallel Programming
  
summary: We explore HPC techniques in the realm of security to improve the speed and increase security. 
---

__Summary__

Steganography and encryption are two methods of securing digital data.
Steganography involves hiding data in other data while encryption involves
making data unreadable.  None of these methods result in 100% security and there
exists techniques and ways to recover secret data that is either hidden by
steganography or jumbled up by encryption.  Time is the limiting factor when in
comes to security and data is, generally, considered more secure if the time it
takes to brute force the data is extremely long.  More secure encryptions are
possible but sometimes they are not worth the time and resources it takes to
encode and decode the secret data.

**Contributions**

<!--center>
<table class="ui fluid floated right medium image"> <caption
align="bottom">Visual representation of our data securing protocol </caption>
<tr><td><img src="/assets/images/projects/stega.png" /></td></tr> </table>
</center-->

In this project with [Ryan Tanaka](https://ryantanaka.github.io/) we propose a
fast method to both hide and secure secret data.  We explore combining
steganography with encryption to add another level of security to our data.
Individuals attempting to recover our secret data would have to first recognize
that data is present.  If they were able to discern if secret data is present,
it will still be in an unreadable form and they would be required to break the
encryption.  We take secret text data, encrypt it, then hide it within different
parts of an image.  This process can be lengthy however, we leverage
multi-threading to help us parallelize this process.  Most encryption algorithms
are heavily data dependent and are not able to be parallelized.  The use of
steganography grants us more security and presents an avenue for us to exploit
parallelization and runtime speedups.   

We implemented our algorithm in C++ with the help of OpenCV.  Experiments on an
8 and 16 core machine to evaluate speed up and how different number of threads
affect performance.  Parallel programming also presents with many unique bugs
that aren't present in sequential code.  We tested the correctness by encoding a
message with our protocol and seeing if we could recover that same message by
our decoding protocol.  To evaluate whether our steganographic hiding of our
message in an image was effective we performed a mean squared error and least
significant bit analysis.  

__Learned__

Prior to this project my experience in security was minimal.  With this project
I was able to learn more about cryptography and encryption.  I learned about
different encryption algorithms when we were trying to determine what to use;
these included AES, DES, and RSA.  I also improved upon my parallel programming
skills when dealing with the parallel steganographic encoding.  I gained some
experience with image processing with OpenCV.  Testing, debugging, and running
experiments are also skills that were practiced and improved upon during this
project.

* Paper to be submitted. Code, algorithm, and results available upon email
* request.
  
<br/>
