# Tech Context: exo

## Core Technologies

- **Python**: The primary language for the project. Requires Python >= 3.12.0.
- **MLX**: An array framework for Apple silicon, used as one of the inference engines.
- **tinygrad**: A lightweight deep learning framework, used as another inference engine.
- **gRPC**: A high-performance RPC framework used for peer-to-peer communication between nodes.
- **Hugging Face**: Models are downloaded from the Hugging Face hub.

## Key Dependencies

- **numpy**: For numerical operations.
- **asyncio**: For asynchronous programming, which is central to the P2P networking.
- **yapf**: For code formatting.

## Inference Engines

Exo supports multiple inference engines, allowing it to run on a variety of hardware:

- **MLX**: For Apple Silicon (macOS).
- **tinygrad**: For a wide range of devices, including Linux and CPUs.
- **PyTorch**: In development.
- **llama.cpp**: Planned.

## Discovery Modules

Exo can discover other devices using several methods:

- **UDP**: For automatic discovery on the local network.
- **Manual**: For manually configuring the network topology.
- **Tailscale**: For discovering devices across different networks using Tailscale.
- **Radio/Bluetooth**: Planned.

## Development Setup

1. **Prerequisites**:
   - Python >= 3.12.0
   - For NVIDIA GPUs on Linux: NVIDIA driver, CUDA toolkit, cuDNN library.
2. **Installation**:
   - Clone the repository: `git clone https://github.com/exo-explore/exo.git`
   - Install in editable mode: `pip install -e .`
3. **Formatting**:
   - Install formatting requirements: `pip3 install -e '.[formatting]'`
   - Run the formatting script: `python3 format.py ./exo`
