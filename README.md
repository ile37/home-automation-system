# Home Automation System Project

**Notice**: This project is intended as a learning resource and not for practical use. There are more robust options available for those seeking a comprehensive home automation solution.

## Introduction

This project presents a lightweight approach to home automation using a standard computer filesystem to organize the layout of your home. Designed specifically for Linux operating systems, it leverages the robustness of Linux's file system and command-line utilities, focusing on simplicity and efficiency with the use of esp32 boards.

## System Architecture

Below is a screenshot illustrating the system architecture in a tree format:

![Screenshot of the system architecture](./setup/help/images/system_architecture_tree_format.png "System Architecture")

## Getting Started

### System uses

- **Linux Operating System**: The system is designed to work on a Linux distribution.
- **Arduino CLI**: Necessary for compiling and uploading sketches to esp32 boards. Place the `arduino-cli` executable in the `./setup/Arduino` folder. Provides a command-line interface for working with Arduino. [Official Arduino CLI documentation](https://arduino.github.io/arduino-cli/latest/).
- **Eclipse Mosquitto**: An MQTT broker that facilitates message queuing for automation tasks. [Download and setup guidance](https://mosquitto.org/download/).
- **Python 3**: Used for running scripts. Ensure Python 3 is available on your system.

### Installation

#### Clone the Repository

To get started with the home automation system, first, clone the repository to your local machine:

#### Setup Environment

1. **Arduino CLI**: Download `arduino-cli` from its [official GitHub repository](https://github.com/arduino/arduino-cli) make sure the executable is located in `./setup/Arduino/`.

2. **Eclipse Mosquitto**: Install Eclipse Mosquitto by following the instructions on the [official Mosquitto website](https://mosquitto.org/download/).

### Esp32 first-time Setup

For the first-time connection of a new esp32 board, use the `-usb` flag to switch to USB port upload. Subsequent uploads can be done normally without the `-usb` flag by leveraging the Arduino OTA library. IP addresses are stored in the `esp32_hostname_log.json` file.

### Automatic Tracking

The system automatically keeps track of connected esp32 boards in the `esp32_hostname_log.json` file, simplifying device management. If `-usb` flag is not found the system automatically searches the `esp32_hostname_log.json` file for the correct port, returns an error if none is found.

## Usage

After installing and setting up your system, devices can be managed through the filesystem by organizing Arduino sketches in the home directory.