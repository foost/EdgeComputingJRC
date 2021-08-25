# EdgeComputingJRC

This repository contains all code to deploy the proof of concept developed under contract by the JRC. 


# License and funding

The work on this proof-of-concept has been commissioned and funded by the European Commission Joint Research Center. However, the type of application, choice of hardware and software, and most importantly mistakes and shortcomings are all my own. More information on the experiment will be forthcomign in a JRC Technical report chapter, to be published at the end of 2021. 

The license is EU Public License 1.2, which is a very permissive license. 

The code in this repository is a proof-of-concept, nothing more. The performance of the model under real-life circumstances is much lower than during the model validation, and the code itself has not been optimized at all. So there is lots of room for forks to improve!


# Files

workflow_documentation.txt
an overview of the workflow used in the experiment, including when to use which script. 

requirements_{conda,pip}.txt
the libraries used in the Python virtual environment

prepare_esc50.ipynb
the script to prepare the input data

train_micro_speech_model_esc50.ipynb
the script where the magic happens. Based on examples for the TinyML book and modified for ESC50 data. 

ble_mqtt_bridge.py
script to connect with BLE Arduino project (see below), to receive detected noise events via BLE, and to publish them via MQTT

mqtt_ecs50_subscribe.ipynb
short script to connect to MQTT service

Arduino_Nano_{BLE_}ESC50_helicopter_siren
ready-to-deploy Arduino Nano code, one using BLE to transmit detected noise events. 

models
Directory containing pre-trained models from the experiments, with meta-data. Can be plugged into the Arduino code, but make sure to adapt all dependent parameters. 
