# Computational Physics MicroPython libraries

## Introduction
This repo contains MicroPython code developed to support computational physics in a laboratory setting, mainly reading data from sensors and displaying results.

## Concept of unified and simplified drivers/modules

In order to make computational physics laboratory activities an enjoyable experience for students and instructors, the developer(s) have made simplified drivers that focus on the key features of sensors with a unified interface among sensors of the same type.

For instance, LIS3HD and ADX345 are 3-axis accelerometers made by different companies with different accuracy and features that make them not exactly interchangeable. But by the magic of unification, regardless which accelerometer you choose to use, a call to accelerometer.read_mss() will always return a tuple of accelerations (actually, force over a fixed mass) in m/s/s unit such as (0.15,-0.23,9.72).

In pursuing for this unified interface for a beginner's sake, the differences among sensors of the same type are NOT addressed, such as some accelerometers have up to 400Hz data rate and others have extended range such as +-16g, yet some can detect knock, double click, issue interrupts under certain conditions (such as free falling). This is definitely an oversimplification of what each sensor can do.

The outcome is hopefully a quick way to utilizing the sensors with minimal efforts.

Also, those who are curious about how these sensors work will find the oversimplified drivers/modules code much easier to understand compared with a more "full feature" driver. In each case, the user is strongly encouraged to consult the sensor's specification sheet. 

To address the omission of some sensor features, other github repos that have "full feature" drivers/modules are included as submodules. These have been tested to work on at least one MicroPython platform, i.e. RP2040, if not more.

## A warning:

Compared with the more unified writing styles of the drivers/modules, the included submodules were all written by different developers, each having their own stypes and conventions. It is like watching YouTube videos of physics lectures from different professors. Each one has their own symbols and styles so it could be disorienting for beginners. Reading the unified drivers/modules code before a "full feature" module is highly recommended. No support is provided for any submodules.

## Convention:

Any files or folders named Driver_[git_handle]_[sensor_model] is a unified and simplified driver/module. Example: Driver_LiuDr_LIS3DH.py

## Installation:

Cloning this repo is highly recommended but for simplicity you can just download the repo in a .zip file. Copy lib folder to the root folder of your MicroPython board. Be mindful how many external submodules you are copying. The recommendation is to not copy anything in lib that doesn't start with Driver_[git_handle].

Example code is in the top-level folder and can be copied to the root folder of your MicroPython board. Example: copy LIS3DH_SH1117_display.py to your board. All example code are written for Adafruit KB2040 board. It is small, inexpensive, and has a large file storage, albeit not a RAM size. [KB2040](https://www.adafruit.com/product/5302)

If you are using a different board, open the code and make necessary changes to the 'i2c=I2C(...)' line to match your board. Then run this code in Thonny. 
