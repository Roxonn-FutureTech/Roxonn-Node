# Product Context: exo

## Problem Solved

Many developers, researchers, and AI enthusiasts are limited by the hardware they own. Running large, powerful AI models requires expensive, specialized hardware that is out of reach for most. Exo addresses this by allowing users to pool the resources of their existing, everyday devices to create a powerful, distributed AI cluster.

## How it Works

Exo works by creating a peer-to-peer network of connected devices. When a user wants to run a model, exo dynamically partitions the model and distributes it across the available devices. Each device processes a portion of the model, and the results are combined to produce the final output. This allows users to run models that are much larger than what any single device could handle on its own.

## User Experience Goals

- **Simplicity**: The user experience should be as simple as possible. Ideally, users should be able to install and run exo with a single command, without any complex configuration.
- **Accessibility**: Exo should be accessible to a wide range of users, from experienced AI developers to hobbyists with limited technical knowledge.
- **Flexibility**: Users should be able to easily add or remove devices from their cluster, and the system should dynamically adapt to these changes.
- **Performance**: While not expecting supercomputer performance, the system should be performant enough to be useful for a variety of tasks.
