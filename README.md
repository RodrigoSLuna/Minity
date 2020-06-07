# Minity

![alt text](https://github.com/RodrigoSLuna/Framework/blob/master/logo/minity.png?raw=true)

	A framework Minity cria um ambiente virtual controlado para realizar extrair métricas na comunicação e na transferencia
	de dados entre as máquinas virtuais. Utilizada para verificar o comportamento dos algoritmos da camada de Transporte do modelo OSI.
	Inicialmente ela foi projetada para realizar experimentos para algoritmos TCP, em especial o TCP BBR	


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

[Learning to learn for global optimization of black box functions](http://www.cantab.net/users/yutian.chen/Publications/ChenEtAl_NIPS16Workshop_L2LBlackBoxOptimization.pdf)

[Easing non-convex optimization with neural networks](https://openreview.net/pdf?id=rJXIPK1PM)

[Neural Generative Models for Global Optimization with Gradients](https://arxiv.org/abs/1805.08594)

[An Introduction and Survey of Estimation of Distribution Algorithms](http://www.medal-lab.org/files/2011004_rev1.pdf)

[The CMA Evolution Strategy: A Tutorial](https://arxiv.org/abs/1604.00772)

[COCO (COmparing Continuous Optimisers)](http://coco.gforge.inria.fr/)

[Taking the Human Out of the Loop: A Review of Bayesian Optimization](https://ieeexplore.ieee.org/document/7352306/)

[Pratical Bayesian Optimization of Machine Learning Algorithms](https://arxiv.org/pdf/1206.2944.pdf)

[Black-Box Variational Inference for Stochastic Differential Equations](http://proceedings.mlr.press/v80/ryder18a.html)

[Guided evolutionary strategies: escaping the curse of dimensionality in random search](https://arxiv.org/abs/1806.10230)

