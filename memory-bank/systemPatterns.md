# System Patterns: exo

## Architecture: Peer-to-Peer (P2P)

Exo utilizes a peer-to-peer architecture, where each device in the network is a "node." There is no central master node; all nodes are equal and communicate directly with each other. This makes the system more resilient and scalable.

## The Node (`exo/orchestration/node.py`)

The `Node` class is the heart of the exo system. Each node is responsible for:

- **Device Discovery**: Using a `Discovery` module, nodes can automatically find other nodes on the network.
- **Peer Communication**: Nodes communicate with each other through `PeerHandle` objects, which are managed by a `Server`.
- **Inference**: Each node has an `InferenceEngine` that can run a portion (a "shard") of an AI model.
- **Topology Management**: Nodes maintain a `Topology` of the network, which is a map of all the nodes and their connections. This topology is updated periodically.
- **Orchestration**: Nodes coordinate with each other to process prompts and tensors, forwarding them to the appropriate node in the network based on the model partitioning.

## Model Partitioning

Exo needs to split large models across the available devices. This is handled by a `PartitioningStrategy`.

### Ring Memory-Weighted Partitioning (`exo/topology/ring_memory_weighted_partitioning_strategy.py`)

This is the default strategy. It works as follows:

1. **Sort Nodes**: The nodes in the network are sorted by their available memory in descending order.
2. **Calculate Proportions**: The total memory of the cluster is calculated. Each node is assigned a proportion of the model based on its memory relative to the total.
3. **Create Partitions**: The model is partitioned into a "ring," and each node is assigned a contiguous block of the model layers proportional to its memory.

This strategy ensures that more powerful devices are given a larger share of the model, optimizing the use of available resources.
