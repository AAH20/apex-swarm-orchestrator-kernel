"""
Apex Hierarchical Swarm Orchestrator and Leader Agent Kernel.
Zero external pip dependencies. Pure Python 3.10+.
"""

__version__ = "0.1.0"
__author__ = "Ahmed Hassan"

from apex_swarm_orchestrator_kernel.engine import (
    ApexSwarmOrchestratorEngine,
    generate_synthetic_swarm_state,
)

__all__ = [
    "ApexSwarmOrchestratorEngine",
    "generate_synthetic_swarm_state",
]
