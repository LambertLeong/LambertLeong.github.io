---
layout: project
type: project
published: trie
image: images/stega.png
title: Parallel Steganographic Encryption
permalink: projects/parallel_steganographic_encryption
date: 2018
labels:
 
  - Steganography
  - Encryption 
  - OpenCv
  - C/C++
  - Parallel Programming
  
summary: We explore HPC techniques in the realm of security to improve the speed and increase security. 
---

__Summary__

Steganography and encryption are two methods of securing digital data. Steganography involves hiding data in other data while encryption involves making data unreadable.  None of these methods result in 100% security and there exists techniques and ways to recover secret data that is either hiden by steganography or jumbled up by encryption.  Time is the limiting factor when in comes to security and data is, generally, considered more secure if the time it takes to brute force the data is extremely long.  More secure encryptions are possible but sometimes they are not worth the time and resources it takes to encode and decod the secret data.

**Contributions**


<table class="ui fluid floated right medium image">
<caption align="bottom">Visual representation of our data securing protocol
</caption>
<tr><td><img src="../images/stega.png" /></td></tr>
</table>
In this project with [Ryan Tanaka](https://ryantanaka.github.io/) we propose a fast method to both hide and secure secret data.  We explore combining steganography with encryption to add another level of security to our data.  Individuals attempting to recover our secret data would have to first recognize that data is present.  If they were able to decern if secret data is present, it will still be in an unreadable form and they would be required to break the encryption.  We take secret text data, encrypt it, then hide it within different parts of an image.  This process can be lengthy however, we leverage multi-threading to help us parallelize this process.  Most encyrption algorithms are heavily data dependant and are unparallelizable.  The use of steganography grants us more security and presents an avenue for us to exploit parallelization and runtime speedups.   

We implemented our algorithm in C++ with the help of OpenCV.  Experiments on an 8 and 16 core machine to evaluate speed up and how differnt number of threads affect performance.  Parallel programming also presents with many unique bugs that arent present in sequential code.  We tested the correctness by encoding a message with our protocol and seeing if we could recover that same message by our decoding protocol.  To evaluate whether our steganographic hiding of our message in an image was effective we performed a mean squared error and least significant bit analysis.  

<!--
__Learned__

Coming Soon-->
