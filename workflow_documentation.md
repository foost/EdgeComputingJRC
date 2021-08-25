# Overview

The workflow to train and use a neural network for audio recognition on an Arduino Nano follows these steps:

0. Hardware and software requirements
1. Prepare/preprocess training data
2. Train model 
3. Adapt and deploy Arduino code
4. Start BLE-MQTT bridge
5. Start MQTT subscription

Each step is briefly described below. More documentation can be found in the notebooks/code, and of course in the TinyML book [1] and Github repository [2]. 


# Hardware and software requirements

This repository used an Arduino Nano BLE Sense for listening to ambient sound and detecting specific noise events. A Raspberry Pi 4B was used as the BLE receiver and MQTT publisher. The model training takes around 90 minutes on a fairly standard quad-core Intel/Win10 laptop. 

The software environment was a Miniconda environment with Python 3.7.11 and Tensorflow 1.15. For details, see the requirements files. 

 
# Prepare training data

The example uses the ESC50 audio data found at [3], but any other data can in principle be used. However, without adapting other parameters, longer audio samples quickly increase the time to train a model and the size of the trained model, and reduce frequency of inference on the Arduino Nano. 

Download and extract the ESC50 data in your working directory, then open the prepare_ESC50.ipynb. Check whether the paths and other parameters are okay for you and run it. Processing takes a couple of minutes at most. 


# Train model

Open the train_micro_speech_model_esc50.ipynb. It is based on the TinyML examples from [2], with modifications to use ESC50 training data. Make sure that all parameters match your intentions (and input data), then run cell-by-cell. The main model building takes around 90 minutes on an average laptop. To check progress, you can open the train directory and see at which learning step it is (or you get Tensorflow Dashboard to work, which I couldn't). 

The output model is a text file, which I suggest to save with a descriptive name and the most important metadata in a separate directory for later reference and reuse. 


# Adapt and deploy Arduino code

The repository contains two Arduino IDE projects for a helicopter and siren model. One is for testing the performance, the other for setting up the BLE-MQTT publishing. It only starts with the inference when connected to a BLE device. 

The important parameters are distributed over several modules. Make sure to check every module even if you have no experience with C++, because every parameter is documented and can be adjusted by just changing the value of the corresponding variable. Tip: change only one variable at a time to observe the effects. First compilation of code takes a bit longer, but after that, compiling and deployment are fast. 

Open the serial monitor to see what the Arduino detects. Don't expect wonders - the model itself has a very good accucary in the validation step, but its performance in real life is much worse (yet - this is where you can step up to the challenge!).


# Start BLE-MQTT bridge

This step only applies when using the BLE version of the code: Start the other BLE device using the ble_mqtt_bridge.py, and choose the correct device to connect with. Once connected, the serial monitor of the Arduino Nano will beging to output the results of inferences. 


# Start MQTT subscription

Open the mqtt_esc50_subscribe.py and run it to subscribe to the detected and published noise events. In case the demonstration server does not work, you can choose another freely available (quick internet search helps). 


# References
[1] https://www.oreilly.com/library/view/tinyml/9781492052036/ 
[2] https://github.com/tensorflow/tflite-micro
[3] https://github.com/karolpiczak/ESC-50
