[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15108800.svg)](https://doi.org/10.5281/zenodo.15108800)

# Project Overview

This project was created for a research project for an course at Toronto Metropolitan University called Intro to Quantum Computing and Quantum Software Engineering. 
This project contains three technical experiments each contributing to understanding the practicality of using Grover's algorithm for key search to break symmetric encryption or finding hash collisions.

# Requirements for the experiments

Requirement: Python 3 (Python 3.9.6 was used but it is likely any Python3 version should be fine)

Under each directory from the project root directory, there is a requirements.txt file that installs the required Python libraries to run that experiment.
This is a complete list of requirements:

- brute_force_classical
  - pycryptodome
  - matplotlib
 
- grover_real_quantum_hardware
  - qiskit>=1
  - qiskit-ibm-runtime>=0.22
  - python-dotenv
  - matplotlib
  * Special additional requirement: Include a .env file in the project directory for specifying your IBM Quantum API key: `IBM_QUANTUM_API_TOKEN=API_KEY`
 
- grover_runtime_analysis (classical simulator)
  - qiskit
  - qiskit-algorithms
  - matplotlib
 
# Running the experiments

From the project root directory, simply execute `python3 ./{subdirectory}/main.py` to run the demonstrations. A matplotlib popup should appear at the end with the figures of the results obtained in the demonstration.
To produce the charts combining all the results, run `python3 ./{subdirectory}/plot_runtime_data.py`.
 
