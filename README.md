# Minity

![alt text](https://github.com/RodrigoSLuna/Framework/blob/master/logo/minity.png?raw=true)

A framework Minity virtualiza um ambiente de redes para a criação de topologias genéricas a fim de verificar a corretude e o comportamento dos algoritmos disponíveis, em especial TCP BBR,  em diversos cenários.


## Installation and Setup (Ubuntu 18.04 LTS):

    ./install.sh

## Running:
    
```
To run Experiment
python2 run.py

To show Plots

python3 run.py
```

## Configuration file (json):

- More information in [cfg_readme.md]

## Visualization and Experiment:

- More information in [info.pdf]


###### Using Minity:

1) Create topology at config.json
2) Create parameters of experiment at params.json
3) Check, test and run Minity
4) Run Analyzer, collector, extract and plot the results
5) Share with anyone .


##### Flow diagram:


##### Directory Structure:

```
.
├── analyzer
│   ├── collectors.py
│   ├── collectors.pyc
│   ├── extractor.py
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── metrics.py
│   ├── __pycache__
│   │   ├── collectors.cpython-37.pyc
│   │   ├── extractor.cpython-37.pyc
│   │   ├── __init__.cpython-37.pyc
│   │   └── metrics.cpython-37.pyc
│   └── tables
│       ├── bbrvalues.csv
│       ├── queuevalues.csv
│       └── sendingrate.csv
├── classes
│   ├── buffer_script.py
│   ├── Client.py
│   ├── Edge.py
│   ├── Edge.pyc
│   ├── Framework.py
│   ├── Framework.pyc
│   ├── Ftp.py
│   ├── Ftp.pyc
│   ├── Handler.py
│   ├── Handler.pyc
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── main.py
│   ├── Network.py
│   ├── Network.pyc
│   ├── Node.py
│   ├── Node.pyc
│   ├── __pycache__
│   │   └── __init__.cpython-37.pyc
│   ├── Router.py
│   ├── Server.py
│   ├── Sniffer.py
│   ├── Sniffer.pyc
│   ├── ss_script.py
│   ├── Switch.py
│   ├── Switch.pyc
│   ├── Topology.py
│   └── Topology.pyc
├── config
│   ├── backup_params.json
│   ├── conf_exp_1.json
│   ├── config.json
│   ├── example_03.json
│   ├── log.txt
│   ├── params_exp_1.json
│   └── params.json
├── Example.py
├── files
│   ├── big_file_2.zip
│   ├── big_file.zip
│   └── file.pdf
├── __init__.py
├── __init__.pyc
├── install.sh
├── logo
│   └── minity.png
├── Parser.ipynb
├── Parser.py
├── __pycache__
│   └── __init__.cpython-37.pyc
├── README.md
├── results
│   ├── h1
│   ├── h2
│   ├── h3
│   ├── h4
│   ├── h5
│   ├── h6
│   ├── sw1
│   ├── sw2
│   └── sw3
└── utils
    ├── algorithms.py
    ├── algorithms.pyc
    ├── __init__.py
    ├── __init__.pyc
    └── __pycache__
        ├── algorithms.cpython-37.pyc
        └── __init__.cpython-37.pyc

```

 - 21 directories, 65 files

### Related Work:
