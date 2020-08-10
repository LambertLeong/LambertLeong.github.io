---
layout: post
cover: assets/images/fun/photo_gallery/all_elements.jpg
title:  The Photographer and Photo Gallery
date: 2018-11-05
categories: fun
author: Lambert
featured: false
permalink: fun/photo-gallery
comments: true
description: "I enjoy being outdoors which includes hiking and going to the beach.  While I am outdoors
 I see many beautiful sights which I try to capture in my photos"
labels:
  - Photography
  - Hawaii
  - Nature
  - Beach
  - Hike
  - Gallery
  - Surf
  - Outdoors
---

test

<!-- Container for the image gallery -->
<div class="container">

  <!-- Full-width images with number text -->
  <div class="mySlides">
    <div class="numbertext">1 / 8</div>
      <img src="/assets/images/fun/photo_gallery/liquid_sunshine.jpg" style="width:100%">
  </div>

  <div class="mySlides">
    <div class="numbertext">2 / 8</div>
      <img src="/assets/images/fun/photo_gallery/undertow_plant.jpg" style="width:100%">
  </div>
  
  <div class="mySlides">
    <div class="numbertext">3 / 8</div>
      <img src="/assets/images/fun/photo_gallery/secret_spot.jpg" style="width:100%">
  </div>
  
  <div class="mySlides">
    <div class="numbertext">4 / 8</div>
      <img src="/assets/images/fun/photo_gallery/all_elements.jpg" style="width:100%">
  </div>

  <div class="mySlides">
    <div class="numbertext">5 / 8</div>
      <img src="/assets/images/fun/photo_gallery/aqua_drops.jpg" style="width:100%">
  </div>

  <div class="mySlides">
    <div class="numbertext">6 / 8</div>
      <img src="/assets/images/fun/photo_gallery/water_color.jpg" style="width:100%">
  </div>

  <div class="mySlides">
    <div class="numbertext">7 / 8</div>
      <img src="/assets/images/fun/photo_gallery/turtle_cave_pano.jpg" style="width:100%">
  </div>

  <div class="mySlides">
    <div class="numbertext">8 / 8</div>
      <img src="/assets/images/fun/photo_gallery/undertow.jpg" style="width:100%">
  </div>

  

  <!-- Next and previous buttons -->
  <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
  <a class="next" onclick="plusSlides(1)">&#10095;</a>

  <!-- Image text -->
  <div class="caption-container">
    <p id="caption"></p>
  </div>

  <!-- Thumbnail images -->
  <div class="row">
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/liquid_sunshine.jpg" style="width:100%" onclick="currentSlide(1)" alt="'Liquid Sunshine' (11x14in canvas)">
    </div>
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/undertow_plant.jpg" style="width:100%" onclick="currentSlide(2)" alt="'Under Tow'  (11x14in canvas)">
    </div>    
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/secret_spot.jpg" style="width:100%" onclick="currentSlide(3)" alt="'Secret Spot'  (11x14in canvas)">
    </div>    
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/all_elements.jpg" style="width:100%" onclick="currentSlide(4)" alt="'All Elements' (11x14in canvas)">
    </div> 
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/aqua_drops.jpg" style="width:100%" onclick="currentSlide(5)" alt="'Aqua Drops' (11x14in canvas)">
    </div>
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/water_color.jpg" style="width:100%" onclick="currentSlide(6)" alt="'Water Color' (11x14in canvas)">
    </div>    
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/turtle_cave_pano.jpg" style="width:100%" onclick="currentSlide(7)" alt="'Turtle Cave' (8x20in Metal)">
    </div>    
    <div class="column">
      <img class="demo cursor" src="/assets/images/fun/photo_gallery/undertow.jpg" style="width:100%" onclick="currentSlide(8)" alt="'Under Tow'  (20x30in & 11x14in canvas)">
    </div>
  </div>
</div>