# Metric FF Planner
See https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html for all the details. Specifically this uses the Metric-FF Version 2.1 (https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF-v2.1.tgz).

Note that the code here is not exactly the same as the one you can download from that website.
Their code had issues that threw segfaults which I was able to fix for this project.
It is possible that my changes caused some other issues that I am unaware of.

First, you will need to compile it
```bash
make
```

To run the sample Pickup/Put problem, run the command:
```bash
sh run_samples.sh
```
