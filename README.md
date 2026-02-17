# AI Pathfinding Visualizer - Assignment 1
**Project Name:** Nexus Grid  
**Author:** [ahmad farooq and tanzeel shazad]  
**Student ID:** [24F-0004  &  24F-0002]

## Overview
This application is a Python-based visualizer for uninformed search algorithms. It features a dynamic environment where obstacles can appear in real-time and includes an advanced computer vision feature to scan maze images into the search grid.

## Features
* **6 Search Algorithms:** BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search.
* **Strict Order:** All algorithms follow a clockwise expansion (Up, Right, Bottom, Bottom-Right, Left, Top-Left, Top-Right, Bottom-Left).
* **Image Scanner:** Upload a maze image (JPG/PNG) to automatically generate a grid.
* **Dynamic Environment:** Real-time obstacle spawning and agent re-planning.
* **Performance Tracking:** Real-time timer and step-by-step animation.

## Installation
1. Install required libraries:
   ```bash
   pip install pygame pygame-gui opencv-python
