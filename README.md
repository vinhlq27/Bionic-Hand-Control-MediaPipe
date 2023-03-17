# Bionic-Hand-Control-MediaPipe

Control a bionic robot hand with your own hand.


## Authors

- [@vinhlq27](https://github.com/vinhlq27)


## Introduction

In 2011, when I was watching a movie called “Real Steel”, I was captivated by the powerful robots that can imitate the activities of the opposite human. This thing has been stuck in my head for years. Back to today’s world, computer vision was growing significantly. We do not need specialized hardwares or powerful processors like it used to be. Moreover, computer vision is widely used in robotics. With advancements like these, the Atom robot from the movie will no longer be a fantasy. In this project, we propose to create a computer vision based system to control a simply bionic hand.

## How To Use

![Signal Flow Chart](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/blob/main/Hand-Design/Signal-Flow.png)

In general, the system works as the above figure demonstrates. A computer processes a video stream to detect a hand and find out which finger is up. Then, this information is sent to a microcontroller to control a bionic hand. We have two main parts:

The system consists of two main parts working together:

- [Python-Code:](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/tree/main/Python-Code) A hand detector that operates on full input images and returns 21 3D landmarks in real-time. Based on these landmarks, the system can figure out which finger is opening.

- [Arduino-Code:](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/tree/main/Arduino-Code) A hand controller that processes on the signals provided by the python code and controls five servos of a bionic hand.

You can find the bionic hand design and circuit diagram in the [Hand-Design](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/tree/main/Hand-Design) file.

The result is showed in the [Demo](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/tree/main/Demo) file. 

![Demo](https://github.com/vinhlq27/Bionic-Hand-Control-MediaPipe/blob/main/Demo/Demo.gif)





