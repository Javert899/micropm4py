# MicroPM4Py

## Introduction

MicroPM4Py is a Python 3/Micropython library that aims to take Process Mining features in power/feature constrained environments, including microcontrollers and embedded systems.

The set of supported features is minimal in comparison to other process mining libraries, like PM4Py, and require no Python dependencies to work.

Official website: [https://www.micropm4py.org](https://www.micropm4py.org)

Micropython website: [https://micropython.org](https://micropython.org)

## Target Hardware

MicroPM4Py can be virtually run on any hardware, even very old or with very low resources/power consumption or embedded systems, since it is compatible with the Python3/Micropython stacks.

MicroPM4Py has been tested at less than 1 MHz on the Unicorn emulator (CPU: Cortex M3, stack: 8 kb, RAM: 64 kb).

MicroPM4Py has been physically tested on a Raspberry Pi 3 B+ (4xA53 @ 1.4 GHz, 1 GB LPDDR2 RAM).

## Installation

On any platform running Python 3: the installation can be easily performed using PIP: pip install -U micropm4py

On Micropython controllers / embedded systems: follow the instructions of your specific board (see the Micropython website). In particular, given the resource constrained environments, some ad-hoc cutting-and-paste of code needs to be done (for example, combining in a single script the XES, PNML and token-based replay).

## Features

Log importing/exporting

* XES importer (level A-1, only case ID and activity)
* XES exporter (level A-1, only case ID and activity)
* CSV importer (only case ID and activity, support for the specification of the separator)
* CSV exporter (only case ID and activity, support for the specification of th separator
* Importing of DFGs from XES (without keeping the log in-memory)
* Importing of DFGs from CSV (without keeping the log in-memory)
* Support for the insertion of artificial start-end activities
* Conversion of log to DFG
* Petri Nets

Execution semantics
* Token-based replay (without support for invisible transitions)
* Importing of PNML files
* Exporting of PNML files
* Conversions

Conversion of DFG to Petri net (DFG mining)
* Conversion of MicroPM4Py DFG to PM4Py DFG
* Conversion from/to MicroPM4Py log to PM4Py log
* Conversion from/to MicroPM4Py Petri nets to PM4Py Petri nets
* Visualizations

Visualizations
* DOT visualization of DFGS
* DOT visualization of Petri nets
