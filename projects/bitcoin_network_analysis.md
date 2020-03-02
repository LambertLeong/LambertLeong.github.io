---
layout: project
type: project
published: true
image: images/projects/btc_network_sample.gif
title: Bitcoin Network Analysis
permalink: projects/bitcoin_network_analysis
date: 2017
labels:
 
  - R
  - Gephi 
  - Data collection/analysis
  - Network Analysis
  - igraph
  - bitcoin
  - blockchain
  
summary: Sampling and network analysis of the rapidly growing Bitcoin exchange and blockchain network. Cover GIF shows growth of the network over 6 hours

---

[__Write up found HERE__](../docs/lleong_snap_shot_samplings_of_the_bitcoin_transaction_network.pdf)

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-4379410432613892"
     data-ad-slot="8398952705"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

__Summary__

In late 2017 Bitcoin, btc, was gaining popularity as the major cryptocurrency
and many began to acquire and exchanges the cryptocurrency.  One of the draws
of btc and other cryptocurrencies is the anonymity that is afforded to the
those involved in transactions.  While all transactions are public and recorded
on the blockchain only addresses and accounts are visible.  Peoples identities
can be detracted from a particular address.  In addition, wallets allowed users
to generate new addresses at, virtually, any time.  

During this period, in 2016, sources claimed that the number of btc users was
growing exponentially.  This trend was also extrapolated to the number of btc
transaction that occurred on the blockchain.  However, during this time btc was
still not respected as an actual currency and it was difficult to exchange it
like money.  As a result we expected to see many users but few interactions
between them.  In this project I took snap shots of the blockchain and
performed network analyses to characterize the network, behavior, and explore
hypotheses and claims made about the network. 

**Contributions**

<table class="ui fluid large floated left image">
<caption align="bottom">Power-law analysis looking for scale free networks with igraph and R.
</caption>
<tr><td><img src="../images/projects/powerlaw_btc.png" /></td></tr>
</table>

<br/>

Using a websocket API provided by
[Blockchain.info](https://www.blockchain.com/api) I was able to sample
blockchain transaction data which included, sender/receiver addresses, amount,
hash difficulty, etc.  I was only concerned with the sender, receiver, and the
amount of btc sent.  I took three samples of the network which included a one,
two, and six hour sample.  The data, containing a little over 13,000 records
was parsed and converted into a .graphml file for analysis.  Using the igraph
package with R I looked at the following network characteristics, transitivity,
average degree, average distance, reciprocity, degree distribution, and maximal
cliques.  In addition, on the largest network, I evaluated community
structures.

<!--figure>
<div class="ui images">
  <img class="ui image medium right floated round image" src="../images/btc_comms.gif">
  <caption alight="bottom">caption</caption>
  <figcaption>This is the figure caption</figcaption>
</div>
</figure-->

<table class="ui fluid large floated right image">
<caption align="bottom">Two biggest community structures visualized using Gephi
</caption>
<tr><td><img src="../images/projects/linkcomzoom.png" /></td></tr>
</table>
<br/>

The graph file was then ported over to [Gephi](https://gephi.org/) mainly for
visualization purposes.  Network analysis was also performed with Gephi because
previous experiences taught me that Gephi metrics vary slightly from those
gather by igraph.  Gephi and igraph sometimes, for certain network metrics,
utilize slightly different algorithms and thus, different values result.  Gephi
helped with the visualization of influential players in the network as well as
community structures.

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-4379410432613892"
     data-ad-slot="8398952705"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

__Learned__

From my work on this project I was able to analyze the btc network and
characterize it.  More importantly, I was able to develop skills in working
with API's, parsing large data, analyzing that data, and presenting it with
visual aids such as igraph and Gephi.  These skills are applicable in many
other situations that require the gathering, analysis, and
presentation/visualization of large amounts of data.  R is a powerful
statistics tool and I foresee my skills with it being useful in my pursuit
toward data driven research.  Networks are ever present and being able to
recognize and analyze them is an important skill.  

<br/>
