"""
Core Data Models for Apex Hierarchical Swarm Orchestrator and Leader Agent Kernel.
Covers Spectral Graph Clustering, MAP-Elites Evolutionary Archives, Field-Tailored
Evaluation Weights, BLS Threshold BFT Quorum, and O(N log N) Hierarchical Dispatch.
Zero external pip dependencies. Pure Python 3.10+.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional


# ============================================================================
# 1. Swarm Agent & Topology Models
# ============================================================================

@dataclass(slots=True)
class AgentNode:
    agent_id: str
    tier: str  # "TIER_0_DIRECTOR", "TIER_1_ORCHESTRATOR", "TIER_2_LEADER", "TIER_3_WORKER"
    domain: str  # "GRID_INFRASTRUCTURE", "QUANT_FINANCE", "AI_COMPILERS", "CYBER_DEFENSE", "SPATIAL_ROBOTICS"
    capability_vector: List[float]  # [Reasoning, Execution, Verification, Red-Teaming, Synthesizer]
    rtt_ms: float
    security_realm: str
    current_vram_gb: float
    token_budget: int


@dataclass(slots=True)
class AgentCluster:
    cluster_id: str
    leader_agent_id: str
    domain: str
    member_agent_ids: List[str]
    spectral_cohesion_score: float
    intra_cluster_latency_ms: float


@dataclass(slots=True)
class SpectralClusteringReport:
    total_agents: int
    clusters_formed: int
    clusters: Dict[str, List[str]]
    leader_assignments: Dict[str, str]
    eigen_gap: float
    clustering_latency_us: float


# ============================================================================
# 2. MAP-Elites Evolution & Quality-Diversity Models
# ============================================================================

@dataclass(slots=True)
class AgentGenome:
    genome_id: str
    prompt_template_id: str
    tool_schema_ids: List[str]
    temperature: float
    reasoning_depth: int
    cti_threshold_ms: float
    fitness_score: float = 0.0
    latency_descriptor_ms: float = 0.0
    token_descriptor_count: int = 0


@dataclass(slots=True)
class MAPElitesArchiveReport:
    total_evaluations: int
    archive_cells_filled: int
    archive_coverage_pct: float
    best_fitness: float
    pareto_frontier_count: int
    evolution_latency_us: float


# ============================================================================
# 3. Domain Weight Tensors & Evaluation Models
# ============================================================================

@dataclass(slots=True)
class DomainWeightTensor:
    domain_name: str
    w_acc: float
    w_lat: float
    w_cost: float
    w_safe: float
    w_det: float
    admission_threshold: float


@dataclass(slots=True)
class DomainEvaluationReport:
    domain_name: str
    raw_metrics: Dict[str, float]
    weighted_fitness: float
    admission_threshold: float
    admitted: bool
    eval_latency_us: float


# ============================================================================
# 4. BLS BFT Quorum & Consensus Models
# ============================================================================

@dataclass(slots=True)
class BLSQuorumVote:
    voter_id: str
    action_payload: str
    partial_signature: str
    weight: float
    is_byzantine_fault: bool = False


@dataclass(slots=True)
class BFTQuorumReport:
    total_voters: int
    participating_weight: float
    quorum_reached: bool
    aggregated_signature: str
    byzantine_faults_tolerated: int
    quorum_latency_us: float


# ============================================================================
# 5. Hierarchical Routing & Dispatch Models
# ============================================================================

@dataclass(slots=True)
class SwarmTaskRoutingReport:
    task_id: str
    origin_tier: str
    dispatched_tier: str
    route_path: List[str]
    total_latency_ms: float
    tokens_consumed: int
    context_pruned_pct: float
    solve_time_us: float


# ============================================================================
# 6. Master Integration Benchmark Model
# ============================================================================

@dataclass(slots=True)
class ApexSwarmBenchmarkReport:
    total_runtime_ms: float
    timestamp: str
    spectral_clustering_summary: Dict[str, float]
    map_elites_evolution_summary: Dict[str, float]
    domain_evaluation_summary: Dict[str, float]
    bft_quorum_summary: Dict[str, float]
    hierarchical_routing_summary: Dict[str, float]
