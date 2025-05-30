# Rubik's Cube Solver 🎲🔄

![rubiks cube project preview](https://github.com/user-attachments/assets/a4b9ec1e-f684-4547-bf3c-1956d3ecb37f)

This project is a **Rubik's Cube Solver** featuring a **custom-built 3D visualization**, multiple interaction methods, and an **AI-powered solving algorithm**.

## ✨ Features

🔹 **3D Visualization from Scratch** – The cube is rendered using a custom-built graphics engine with smooth animations and realistic interactions.
🔹 **Interactive Controls** – Rotate the cube freely, perform moves manually, or scramble it with a single click.
🔹 **AI Solver** – Automatically solves the cube using optimized algorithms, showing step-by-step animations.
🔹 **Camera-Based Detection Mode** – Use your USB webcam to scan the cube’s six faces in real time, automatically generating the detected state for solving.

## 🆕 Cube Detection Mode

A new **Detection Mode** allows you to scan the real Rubik's Cube using your USB camera. Once activated, the program guides you to show each side of your cube to the camera. The software then detects and captures the color configuration using **deep neural networks** based on the **YOLOv11 object detection model**. Each sticker is accurately identified, and after scanning all six faces, the full cube state is reconstructed virtually—ready to be solved by the AI.

## 🎮 Controls

The project offers intuitive keyboard controls for interacting with the cube:

* **Spacebar** – Pause/resume cube rotation
* **Shift** – Scramble the cube with a random valid sequence
* **Enter** – Trigger the AI solver and begin the animated solution
* **Arrow Keys / Mouse** – Rotate the cube in 3D space
* **Face Turns** – Use specific keys (e.g., `U`, `D`, `L`, `R`, `F`, `B`) to manually rotate cube faces
* **Detection Mode Toggle** – Activate detection mode to begin scanning the cube via webcam

## 🎮 Ways to Interact

✅ **Mouse & Keyboard Controls** – Rotate the cube and execute moves naturally
✅ **Touchscreen Support** – Swipe gestures to manipulate the cube
✅ **Algorithm Execution** – Enter sequences manually or let AI take over
✅ **Camera Detection** – Scan your real cube and solve it virtually

## 🚀 How It Works

1️⃣ **Scramble the Cube** – Generate a random state or use detection mode
2️⃣ **Solve Manually or with AI** – Try solving it yourself or let AI find the optimal solution
3️⃣ **Watch Step-by-Step Animations** – The AI solver demonstrates each move in real-time

Whether you're a beginner looking to explore or an expert speedsolver, this project provides an intuitive and powerful way to interact with and solve the Rubik’s Cube. 🧩🎯

## 🎨 3D Visualization

This project visualizes a Rubik's Cube using Pygame, leveraging manual 3D-to-2D transformation techniques to simulate depth and perspective. Instead of relying on external 3D rendering libraries, the cube's three-dimensional structure is projected onto a 2D plane using basic geometric transformations.

## 🤖 Solving Algorithm

This Rubik’s Cube solver implements a Modified Breadth-First Search (BFS) with structured checkpoints to efficiently reach the solution step by step. Instead of treating the cube as a single search space where all states are equally important, the algorithm breaks the problem into logical milestones. Each milestone represents a significant step in standard solving methods, reducing the overall search complexity and ensuring efficient solving.

## 🧠 Key Idea: Layered BFS with Checkpoints

The modified BFS does not search for a solution in one continuous step. Instead, it follows a layered approach, progressing through checkpoints in a defined order. Each checkpoint represents a major milestone in solving the cube. Additionally, every checkpoint comes with its own predefined algorithms, so that the possible moves to get from one checkpoint to the next are significantly reduced.

## 📈 Advantages of the Checkpoint-Based BFS Approach

✅ **More efficient than a naive brute-force BFS** – reduces the search space significantly

✅ **Follows human-like solving intuition** – aligns with common beginner and advanced solving techniques

✅ **Easier to debug and visualize** – because it progresses through structured stages

✅ **Optimized move count** – by focusing only on the moves necessary for the current milestone

# 🔥 **Try it out and let’s solve the cube!** 🔥
