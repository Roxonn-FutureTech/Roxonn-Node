# Project Progress: exo

## What Works

- **Core Functionality**: The core functionality of the exo system is in place. This includes device discovery, P2P communication, and distributed inference.
- **Inference Engines**: The MLX and tinygrad inference engines are supported, enabling exo to run on a variety of hardware.
- **Model Support**: A range of popular models are supported, including LLaMA, Mistral, and Deepseek.
- **API**: A ChatGPT-compatible API is available for developers.
- **Web UI**: A basic web UI is available for interacting with the system.

## What's Left to Build

- **Additional Inference Engines**: Support for PyTorch and llama.cpp is in development.
- **Additional Discovery Modules**: Support for Radio and Bluetooth discovery is planned.
- **iOS Implementation**: The iOS implementation is currently out of date and needs to be updated.
- **Improved Stability**: As the project is experimental, there are likely to be bugs and stability issues that need to be addressed.
- **Enhanced UI/UX**: The web UI is basic and could be improved with more features and a better user experience.

## Known Issues

- **SSL Certificate Errors on macOS**: On some versions of Python on macOS, SSL certificates may not be installed correctly, which can cause errors when downloading models from Hugging Face.
- **iOS Implementation is Behind**: The iOS implementation is not up-to-date with the Python version and is not currently recommended for use.

## Project Evolution

- The project is actively evolving, with new features and improvements being added regularly.
- The focus is on building a robust and user-friendly system for distributed AI.
- Community contributions are encouraged to help accelerate development.
