# 🧠 Nexus Grid  
## AI Pathfinding Visualizer

**Author:** Ahmad Farooq  
**Course:** Artificial Intelligence  
**Project Type:** Uninformed Search Algorithm Visualizer  

---

## 📌 Overview

**Nexus Grid** is a Python-based interactive visualization platform designed to demonstrate and analyze uninformed search algorithms within a dynamic grid environment.

The system goes beyond traditional static visualizers by integrating:

- Real-time obstacle generation  
- Intelligent agent re-planning  
- Image-based maze scanning using computer vision  

This project bridges theoretical AI search strategies with practical implementation and interactive visualization.

---

## 🚀 Features

### 🔎 Implemented Algorithms

The application supports six uninformed search algorithms:

- Breadth-First Search (BFS)  
- Depth-First Search (DFS)  
- Uniform Cost Search (UCS)  
- Depth-Limited Search (DLS)  
- Iterative Deepening Depth-First Search (IDDFS)  
- Bidirectional Search  

---

### 🔄 Deterministic Expansion Order

All algorithms strictly follow a **clockwise expansion strategy**:

Up → Right → Bottom → Bottom-Right → Left → Top-Left → Top-Right → Bottom-Left  

This ensures consistent, reproducible behavior across all search methods.

---

### 🖼️ Image-Based Maze Scanner

Users can upload a maze image (JPG/PNG). The system:

- Processes the image using OpenCV  
- Converts it into a binary grid  
- Automatically initializes the search environment  

This demonstrates the integration of computer vision with AI pathfinding.

---

### ⚡ Dynamic Environment Simulation

- Real-time obstacle spawning  
- Agent re-planning during execution  
- Continuous search state updates  

This simulates realistic, evolving environments.

---

### 📊 Performance Tracking

- Real-time execution timer  
- Step-by-step animation  
- Path reconstruction visualization  

These features allow performance comparison across algorithms.

---

## 🛠️ Technology Stack

- Python  
- Pygame  
- Pygame GUI  
- OpenCV  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/nexus-grid.git
cd nexus-grid
