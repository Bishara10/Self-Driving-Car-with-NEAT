# Self Driving Car with NEAT

This project uses the [NEAT](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf) (NeuroEvolution of Augmenting Topologies) algorithm to evolve neural networks that learn to play a game built with Pygame. Using a genetic algorithm approach, NEAT evolves neural networks over successive generations to learn driving behaviors such as steering, acceleration, and obstacle avoidance.

The simulation is built with Pygame, providing a visual and interactive platform where the AI-controlled car learns to navigate through a track by optimizing its performance through evolutionary principles, without any hard-coded rules.

Neural networks are evolved using the `neat-python` library and visualized with Graphviz.


## 🧠 About NEAT

NEAT is a genetic algorithm for evolving artificial neural networks. It starts with simple networks and complexifies them through mutations over generations, optimizing both weights and topologies.
Problems Solved by NEAT

1. **Meaningful crossover of networks with different topologies** by tracking historical gene origins.

2. **Protecting new structural innovations** through speciation to avoid premature loss.

3. **Incremental growth of network complexity**, starting simple and adding complexity only when needed.

These features enable efficient and effective evolution of autonomous driving behaviors.

> Read the NEAT paper here:  
> 📄 [Evolving Neural Networks through Augmenting Topologies (Stanley & Miikkulainen, 2002)](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf)


## 🕹️ Gameplay

The game is implemented with `pygame`. Each neural network controls a car. The game loop evaluates fitness for each agent and selects the fittest networks to reproduce for the next generation.

---

## 📦 prerequisites

### Graphviz

Graphviz is required for visualizing the neural networks.

1. Download and install Graphviz from:  
   🔗 https://graphviz.org/download/

2. Add Graphviz to your system `PATH`:
   - There's an option during the installation process to automatically add it to system `PATH`.
   
   if missed:
   - **On Windows**: Add the `bin/` folder of the Graphviz installation to your system’s environment `PATH` variable.  
   - **On macOS/Linux**: Graphviz is often added automatically, or you can install it via Homebrew or your package manager.

---

## 🚀 Getting Started

1. Clone the repository:

  ```bash
  git clone https://github.com/Bishara10/Self-Driving-Car-with-NEAT.git
  cd Self-Driving-Car-with-NEAT
  ```

2. Install the required Python libraries from requirements.txt:

  ```bash
  pip install -r requirements.txt
  ```

3. Run the Training Loop

  ```bash
  python main.py
  ```
