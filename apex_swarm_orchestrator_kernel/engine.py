"""
Unified Coordination Engine for Apex Hierarchical Swarm Orchestrator Kernel.
Orchestrates Spectral Graph Clustering, MAP-Elites Evolutionary Archives, Field-Tailored
Evaluation Weights, BLS BFT Quorum Consensus, and O(N log N) Hierarchical Mission Routing.
Zero external pip dependencies. Pure Python 3.10+.
"""

from __future__ import annotations
import datetime
import time
from typing import List, Dict, Set, Tuple, Optional

from apex_swarm_orchestrator_kernel.core.models import (
    AgentNode,
    AgentCluster,
    SpectralClusteringReport,
    AgentGenome,
    MAPElitesArchiveReport,
    DomainWeightTensor,
    DomainEvaluationReport,
    BLSQuorumVote,
    BFTQuorumReport,
    SwarmTaskRoutingReport,
    ApexSwarmBenchmarkReport,
)
from apex_swarm_orchestrator_kernel.core.spectral_clustering_engine import (
    SpectralClusteringEngine,
)
from apex_swarm_orchestrator_kernel.core.map_elites_evolution_pool import (
    MAPElitesEvolutionPool,
)
from apex_swarm_orchestrator_kernel.core.domain_weights_arbiter import (
    DomainWeightsArbiter,
)
from apex_swarm_orchestrator_kernel.core.bls_bft_quorum_arbiter import (
    BLSBFTQuorumArbiter,
)
from apex_swarm_orchestrator_kernel.core.swarm_hierarchical_router import (
    SwarmHierarchicalRouter,
)


def generate_synthetic_swarm_state() -> Tuple[
    List[AgentNode],
    List[AgentGenome],
    Dict[str, float],
    List[BLSQuorumVote],
    str,
]:
    """
    Generates realistic 24-agent hierarchical swarm state spanning all 4 tiers and 5 domains.
    """
    domains = [
        "GRID_INFRASTRUCTURE",
        "QUANT_FINANCE",
        "AI_COMPILERS",
        "CYBER_DEFENSE",
        "SPATIAL_ROBOTICS",
    ]

    agents: List[AgentNode] = []

    # Tier 0: Sovereign Metacognitive Director
    agents.append(
        AgentNode(
            agent_id="agent_tier0_director_sovereign",
            tier="TIER_0_DIRECTOR",
            domain="GRID_INFRASTRUCTURE",
            capability_vector=[0.98, 0.92, 0.99, 0.95, 0.99],
            rtt_ms=1.2,
            security_realm="REALM_SOVEREIGN_ROOT",
            current_vram_gb=80.0,
            token_budget=1_000_000,
        )
    )

    # Tier 1: Domain Cluster Orchestrators
    for d in domains:
        agents.append(
            AgentNode(
                agent_id=f"agent_tier1_orch_{d.lower()}",
                tier="TIER_1_ORCHESTRATOR",
                domain=d,
                capability_vector=[0.94, 0.88, 0.92, 0.85, 0.96],
                rtt_ms=3.5,
                security_realm="REALM_ENCLAVE_ALPHA",
                current_vram_gb=48.0,
                token_budget=500_000,
            )
        )

    # Tier 2: Squad Leaders
    for d in domains:
        agents.append(
            AgentNode(
                agent_id=f"agent_tier2_leader_{d.lower()}_squad",
                tier="TIER_2_LEADER",
                domain=d,
                capability_vector=[0.89, 0.92, 0.88, 0.82, 0.90],
                rtt_ms=6.8,
                security_realm="REALM_ENCLAVE_ALPHA",
                current_vram_gb=32.0,
                token_budget=250_000,
            )
        )

    # Tier 3: Tactical Worker Agents
    worker_idx = 0
    for d in domains:
        for _ in range(2):
            agents.append(
                AgentNode(
                    agent_id=f"agent_tier3_worker_{d.lower()}_{worker_idx:02d}",
                    tier="TIER_3_WORKER",
                    domain=d,
                    capability_vector=[0.75, 0.95, 0.80, 0.70, 0.78],
                    rtt_ms=12.5 + (worker_idx % 3),
                    security_realm="REALM_ENCLAVE_ALPHA",
                    current_vram_gb=16.0,
                    token_budget=100_000,
                )
            )
            worker_idx += 1

    # Initial seed genomes for MAP-Elites
    seed_genomes: List[AgentGenome] = [
        AgentGenome(
            genome_id="seed_genome_01_fast",
            prompt_template_id="tmpl_ultra_low_latency_v1",
            tool_schema_ids=["tool_pmu_read", "tool_fast_shed"],
            temperature=0.10,
            reasoning_depth=2,
            cti_threshold_ms=180.0,
            latency_descriptor_ms=18.5,
            token_descriptor_count=1800,
        ),
        AgentGenome(
            genome_id="seed_genome_02_deep",
            prompt_template_id="tmpl_deep_verification_v3",
            tool_schema_ids=["tool_smt_prove", "tool_cfi_check", "tool_sel_grade"],
            temperature=0.05,
            reasoning_depth=8,
            cti_threshold_ms=220.0,
            latency_descriptor_ms=58.0,
            token_descriptor_count=4500,
        ),
    ]

    # Raw metrics for domain evaluation
    candidate_metrics = {
        "accuracy": 0.985,
        "latency_score": 0.940,
        "cost_score": 0.910,
        "safety_score": 0.995,
        "determinism_score": 0.960,
    }

    # BLS Quorum votes (including 1 adversarial outlier)
    votes: List[BLSQuorumVote] = [
        BLSQuorumVote("voter_01", "ACTUATE_DVFS_SHED_250MW", "sig_share_01_valid", 1.0, False),
        BLSQuorumVote("voter_02", "ACTUATE_DVFS_SHED_250MW", "sig_share_02_valid", 1.0, False),
        BLSQuorumVote("voter_03", "ACTUATE_DVFS_SHED_250MW", "sig_share_03_valid", 1.0, False),
        BLSQuorumVote("voter_04_byzantine", "ACTUATE_CORRUPT_OVERRIDE", "sig_share_04_bad", 1.0, True),
        BLSQuorumVote("voter_05", "ACTUATE_DVFS_SHED_250MW", "sig_share_05_valid", 1.0, False),
    ]

    sample_task_id = "TASK_GIGAWATT_GRID_SHED_001"

    return agents, seed_genomes, candidate_metrics, votes, sample_task_id


class ApexSwarmOrchestratorEngine:
    """
    Unified Algorithmic Engine for Apex Hierarchical Swarm Orchestration.
    """

    def __init__(self):
        self.spectral_clusterer = SpectralClusteringEngine(sigma=1.0, latency_penalty_alpha=0.05)
        self.evolution_pool = MAPElitesEvolutionPool(latency_bins=10, token_bins=10)
        self.weights_arbiter = DomainWeightsArbiter()
        self.quorum_arbiter = BLSBFTQuorumArbiter(quorum_threshold_pct=0.67)
        self.hierarchical_router = SwarmHierarchicalRouter(token_pruning_efficiency_pct=97.2)

    def cluster_and_elect_leaders(
        self, agents: List[AgentNode], target_k: int = 5
    ) -> SpectralClusteringReport:
        """Partitions agents into squads and elects leaders via Shapley values."""
        return self.spectral_clusterer.cluster_agents(agents, target_k)

    def step_map_elites_evolution(
        self, seed_population: List[AgentGenome], cycles: int = 50
    ) -> MAPElitesArchiveReport:
        """Evolves agent genomes across 2D quality-diversity feature space."""
        return self.evolution_pool.step_evolution(seed_population, cycles)

    def evaluate_domain_weights(
        self, domain_name: str, metrics: Dict[str, float]
    ) -> DomainEvaluationReport:
        """Evaluates candidate performance against domain-calibrated weight tensors."""
        return self.weights_arbiter.evaluate_candidate(domain_name, metrics)

    def verify_bft_quorum(
        self, votes: List[BLSQuorumVote], payload: str
    ) -> BFTQuorumReport:
        """Aggregates BLS threshold shares while pruning Byzantine outlier votes."""
        return self.quorum_arbiter.verify_and_aggregate_quorum(votes, payload)

    def route_hierarchical_mission(
        self, task_id: str, domain: str, agents: List[AgentNode]
    ) -> SwarmTaskRoutingReport:
        """Traverses the 4-tier hierarchy with prefix context pruning."""
        return self.hierarchical_router.route_mission(task_id, domain, agents)

    def run_full_pipeline_benchmark(
        self, iterations: int = 50
    ) -> ApexSwarmBenchmarkReport:
        """
        Executes end-to-end multi-disciplinary benchmark across all 5 swarm solvers.
        """
        start_t = time.perf_counter()
        agents, genomes, metrics, votes, task_id = generate_synthetic_swarm_state()

        # 1. Benchmark Spectral Clustering
        cluster_times: List[float] = []
        cluster_reports: List[SpectralClusteringReport] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            r = self.cluster_and_elect_leaders(agents, 5)
            cluster_times.append((time.perf_counter() - t0) * 1_000_000.0)
            cluster_reports.append(r)
        last_cluster = cluster_reports[-1]

        # 2. Benchmark MAP-Elites Evolution
        evo_times: List[float] = []
        evo_reports: List[MAPElitesArchiveReport] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            r = self.step_map_elites_evolution(genomes, 20)
            evo_times.append((time.perf_counter() - t0) * 1_000_000.0)
            evo_reports.append(r)
        last_evo = evo_reports[-1]

        # 3. Benchmark Domain Weights Evaluation
        eval_times: List[float] = []
        eval_reports: List[DomainEvaluationReport] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            r = self.evaluate_domain_weights("GRID_INFRASTRUCTURE", metrics)
            eval_times.append((time.perf_counter() - t0) * 1_000_000.0)
            eval_reports.append(r)
        last_eval = eval_reports[-1]

        # 4. Benchmark BLS BFT Quorum
        quorum_times: List[float] = []
        quorum_reports: List[BFTQuorumReport] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            r = self.verify_bft_quorum(votes, "ACTUATE_DVFS_SHED_250MW")
            quorum_times.append((time.perf_counter() - t0) * 1_000_000.0)
            quorum_reports.append(r)
        last_quorum = quorum_reports[-1]

        # 5. Benchmark Hierarchical Routing
        route_times: List[float] = []
        route_reports: List[SwarmTaskRoutingReport] = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            r = self.route_hierarchical_mission(task_id, "GRID_INFRASTRUCTURE", agents)
            route_times.append((time.perf_counter() - t0) * 1_000_000.0)
            route_reports.append(r)
        last_route = route_reports[-1]

        total_runtime_ms = (time.perf_counter() - start_t) * 1000.0

        return ApexSwarmBenchmarkReport(
            total_runtime_ms=round(total_runtime_ms, 2),
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            spectral_clustering_summary={
                "avg_solve_latency_us": round(sum(cluster_times) / len(cluster_times), 2),
                "clusters_formed": float(last_cluster.clusters_formed),
                "total_agents": float(last_cluster.total_agents),
                "eigen_gap": float(last_cluster.eigen_gap),
            },
            map_elites_evolution_summary={
                "avg_solve_latency_us": round(sum(evo_times) / len(evo_times), 2),
                "archive_coverage_pct": float(last_evo.archive_coverage_pct),
                "best_fitness": float(last_evo.best_fitness),
                "pareto_frontier_count": float(last_evo.pareto_frontier_count),
            },
            domain_evaluation_summary={
                "avg_solve_latency_us": round(sum(eval_times) / len(eval_times), 2),
                "weighted_fitness": float(last_eval.weighted_fitness),
                "admitted": 1.0 if last_eval.admitted else 0.0,
            },
            bft_quorum_summary={
                "avg_solve_latency_us": round(sum(quorum_times) / len(quorum_times), 2),
                "quorum_reached": 1.0 if last_quorum.quorum_reached else 0.0,
                "byzantine_faults_tolerated": float(last_quorum.byzantine_faults_tolerated),
            },
            hierarchical_routing_summary={
                "avg_solve_latency_us": round(sum(route_times) / len(route_times), 2),
                "tokens_consumed": float(last_route.tokens_consumed),
                "context_pruned_pct": float(last_route.context_pruned_pct),
                "total_latency_ms": float(last_route.total_latency_ms),
            },
        )
