# EdgeComputingJRC

This repository contains all code to deploy the proof of concept developed under contract by the European Commission's Joint Research Center [1]. 


# License and funding

Although the work on this proof-of-concept has been commissioned and funded by the JRC, the choice of application, hardware, and software, as well as all mistakes and shortcomings are my own, and do not constitute any endorsement by the JRC. More information on the experiment will be forthcoming in a JRC Technical report chapter, to be published at the end of 2021. 

The license is EU Public License 1.2, which is a very permissive license. 

The code in this repository is a proof-of-concept, nothing more. The performance of the model under real-life circumstances is much lower than during the model validation, and the code itself has not been optimized at all. So there is lots of room for forks to improve!


# Files

_0_workflow_documentation.md_

an overview of the workflow used in the experiment, including when to use which script. 


_requirements_{conda,pip}.txt_

the libraries used in the Python virtual environment


_1_prepare_esc50.py_

the script to prepare the input data


_2_train_noise_listener_model_esc50.ipynb_

the script where the magic happens. Based on examples for the TinyML book and modified for ESC50 data. 


_3_ble_mqtt_bridge.py_

script to connect with BLE Arduino project (see below), to receive detected noise events via BLE, and to publish them via MQTT


_4_mqtt_ecs50_subscribe.py_

short script to connect to MQTT service


_Arduino_Nano_{BLE_}ESC50_helicopter_siren_ 

folders with ready-to-deploy Arduino Nano code, one using BLE to transmit detected noise events. 


_models_

folders containing pre-trained models from the experiments, with meta-data. Can be plugged into the Arduino code, but make sure to adapt all dependent parameters. 


# References
[1] https://ec.europa.eu/info/departments/joint-research-centre_en
