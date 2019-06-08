---
layout: project
type: project
published: false
image: images/og-image-logo.png
title: Test
permalink: projects/gantt
date: 2019
labels:
  - JavaScript
  
  
summary: tst

---


We offer services focused on the Apache Spark engine. There are several options regarding the cluster manager, data store, build tools, automation and deployments.

### Spark workflow

All of these tools enable you to quickly develop, configure and deploy applications to a Spark cluster. That way you can spend more time gleaning insights and less time debugging.

{% mermaid %}
graph LR
  C{Application} -.Build.-> C{Application}
    C -.Deploy.-> G(Spark Master)
    subgraph Virtual Environment
    G -.-> D(Spark Worker)
    D -.-> H(Data Store)
    G -.-> E(Spark Worker)
    E -.-> I(Data Store)
    G -.-> F(Spark Worker)
    F -.-> J(Data Store)
  end
{% endmermaid %}
