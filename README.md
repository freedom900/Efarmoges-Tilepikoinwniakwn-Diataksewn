# Efarmoges-Tilepikoinwniakwn-Diataksewn

This repository is created for the Applied Telecommunication Systems course in Aristotle University of Thessaloniki. The project was developed by a team of four students.

## Project Overview

In this project we created a real-time bus occupancy tracking system using motion sensors. The main goal was to provide passengers with live information about how crowded a bus is, allowing them to choose the most suitable bus and bus stop.

The idea originated from the frequent overcrowding on popular bus routes where people would have to wait for the next bus or walk to a different bus stop. This system aims to help in effcient trip planning and reduce congestion inside buses.

## System Architecture
Each bus is represented by an Arduino which collects the motion sensor data and sends them to a central Arduino. There are two motion sensors in each bus entrance and depending on which one is triggered first, the system can determine whether the passenger is entering or exiting the bus.

The central Arduino is connected to a laptop via USB. The data is then parsed by a Python script, which processes and visualises them through a graphical user interface. Using PyQt we recreated a simplified version of our local bus app and modified it to display the real-time data collected.

## Running the project
1. Connect the central Arduino to the laptop
2. Ensure the correct USB port is selected in the Arduino code
3. Upload the Arduino code to all Arduinos
4. Run the Python script to launch the GUI

## Future Improvements
- Use gps system to track the live location of buses
- Store historical occupancy data for analysis and prediction
- Improve sensor system, potentially use cameras for increased accuracy
