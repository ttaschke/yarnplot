# Yarnplot

> Yarnplot is a tool to collect timeline-based statistics about running YARN applications.

Yarnplot allows to track specified statistics (e.g. used VCores or memory) of a YARN application over time
and store the results either as tabular data or as a graph.


* Release 0.1.0 (initial release)
* Python 2.7

### Example output

![](https://user-images.githubusercontent.com/7067750/30961683-fb0f9366-a481-11e7-830e-ff43506476a2.png)


# Installation

Yarnplot can be installed as a commandline tool or executed directly from source after installing its dependencies.


## Commandline tool

```
python setup.py install
```

## Execute from source

```
pip install -r requirements.txt
python -m yarnplot
```

# Usage

* Required arguments
  * Resourcemanager hostname
  * Yarnplot's mode

## List running YARN applications (mode: list)

As a helper function to quickly find the id of an application for tracking, 
Yarnplot provides a method to list all running YARN applications with their id and name.

```
yarnplot resourcemanager.example list
```

## Track statistics of a specific YARN application (mode: app)

Yarnplot by default tracks the resources used by an application, 
but can be configured to track other attributes provided by the YARN Rest API too.

See the YARN Cluster Application API for a complete list of attributes that can be tracked:
https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Application_API

Output options include a plot as `.png` or tabular data as '.csv'.

### Full example

```
yarnplot resourcemaanger.host app -app_id application_111111111111_00001 -cols allocatedVCores allocatedMB numNonAMContainerPreempted progress -output plot -output_folder output -sample_rate 1
```

## CLI options
```
$ yarnplot -h
usage: yarnplot [-h] [-app_id [APP_ID]] [-cols COLS [COLS ...]]
                [-sample_rate [SAMPLE_RATE]] [-output [OUTPUT]]
                [-output_folder [OUTPUT_FOLDER]]
                [host] [mode]

YarnPlot - Tool to collect timeline-based YARN application statistics

positional arguments:
  host                  Resourcemanager hostname
  mode                  mode: list (displays running applications), app
                        (tracks

optional arguments:
  -h, --help            show this help message and exit
  -app_id [APP_ID]      YARN application id. Required for app mode
  -attributes ATTRIBUTES [ATTRIBUTES ...]
                        YARN application attributes to track (e.g. -attributes
                        allocatedVCores progress). See Yarn REST API
                        documentation for full list
  -sample_rate [SAMPLE_RATE]
                        Sample rate in seconds (default: 1). High sample rates
                        are recommend to ensure accuracy)
  -output [OUTPUT]      output mode (plot, csv
  -output_folder [OUTPUT_FOLDER]
                        Existing folder in which to save the output (default:
                        current working directory)
```