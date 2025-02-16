# Rubik's Cube Solver 🎲🔄  
![rubiks cube project preview](https://github.com/user-attachments/assets/a4b9ec1e-f684-4547-bf3c-1956d3ecb37f)

This project is a **Rubik's Cube Solver** featuring a **custom-built 3D visualization**, multiple interaction methods, and an **AI-powered solving algorithm**.  

## ✨ Features  

🔹 **3D Visualization from Scratch** – The cube is rendered using a custom-built graphics engine with smooth animations and realistic interactions.  
🔹 **Interactive Controls** – Rotate the cube freely, perform moves manually, or scramble it with a single click.  
🔹 **AI Solver** – Automatically solves the cube using optimized algorithms, showing step-by-step animations.  

## 🎮 Ways to Interact  

✅ **Mouse & Keyboard Controls** – Rotate the cube and execute moves naturally.  
✅ **Touchscreen Support** – Swipe gestures to manipulate the cube.  
✅ **Algorithm Execution** – Enter sequences manually or let AI take over.  

## 🚀 How It Works  

1️⃣ **Scramble the Cube** – Generate a random state.  
2️⃣ **Solve Manually or with AI** – Try solving it yourself or let AI find the optimal solution.  
3️⃣ **Watch Step-by-Step Animations** – The AI solver demonstrates each move in real-time.  

Whether you're a beginner looking to explore or an expert speedsolver, this project provides an intuitive and powerful way to interact with and solve the Rubik’s Cube. 🧩🎯  

🔥 **Try it out and let’s solve the cube!** 🔥

## 🎨🕹️ 3D Visualization
This project visualizes a Rubik's Cube using Pygame, leveraging manual 3D-to-2D transformation techniques to simulate depth and perspective. Instead of relying on external 3D rendering libraries, the cube's three-dimensional structure is projected onto a 2D plane using basic geometric transformations.

## 🤖🧩 Solving Algorithm
This Rubik’s Cube solver implements a Modified Breadth-First Search (BFS) with structured checkpoints to efficiently reach the solution step by step. Instead of treating the cube as a single search space where all states are equally important, the algorithm breaks the problem into logical milestones. Each milestone represents a significant step in standard solving methods, reducing the overall search complexity and ensuring efficient solving.

### Key Idea: Layered BFS with Checkpoints
The modified BFS does not search for a solution in one continuous step. Instead, it follows a layered approach, progressing through checkpoints in a defined order. Each checkpoint represents a major milestone in solving the cube. Additionally every checkpoint comes with its own predefined algorithms, so that the possible moves to get from one checkpoint to the other, is significantly reduced.

### Advantages of the Checkpoint-Based BFS Approach
✅ More efficient than a naive brute-force BFS – reduces the search space significantly.
✅ Follows human-like solving intuition – aligns with common beginner and advanced solving techniques.
✅ Easier to debug and visualize – because it progresses through structured stages.
✅ Optimized move count – by focusing only on the moves necessary for the current milestone.