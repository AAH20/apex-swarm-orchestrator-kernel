"""
Unit tests for SpectralClusteringEngine.
"""

import unittest
from apex_swarm_orchestrator_kernel.core.models import AgentNode
from apex_swarm_orchestrator_kernel.core.spectral_clustering_engine import (
    SpectralClusteringEngine,
)


class TestSpectralClusteringEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SpectralClusteringEngine(sigma=1.0, latency_penalty_alpha=0.05)
        self.agents = [
            AgentNode(
                agent_id=f"agent_grid_{i}",
                tier="TIER_3_WORKER",
                domain="GRID_INFRASTRUCTURE",
                capability_vector=[0.9 - (i * 0.05), 0.8, 0.7, 0.6, 0.5],
                rtt_ms=10.0 + (i * 2.0),
                security_realm="REALM_ENCLAVE_A",
                current_vram_gb=16.0,
                token_budget=100000,
            )
            for i in range(5)
        ] + [
            AgentNode(
                agent_id=f"agent_quant_{i}",
                tier="TIER_3_WORKER",
                domain="QUANT_FINANCE",
                capability_vector=[0.7, 0.95 - (i * 0.05), 0.6, 0.5, 0.8],
                rtt_ms=2.0 + (i * 0.5),
                security_realm="REALM_ENCLAVE_B",
                current_vram_gb=32.0,
                token_budget=100000,
            )
            for i in range(5)
        ]

    def test_spectral_clustering_and_leader_assignment(self):
        report = self.engine.cluster_agents(self.agents, target_k_clusters=2)

        self.assertEqual(report.total_agents, 10)
        self.assertGreaterEqual(report.clusters_formed, 2)
        self.assertGreater(report.eigen_gap, 0.0)
        self.assertEqual(len(report.leader_assignments), report.clusters_formed)
        self.assertLess(report.clustering_latency_us, 5000.0)

    def test_empty_agent_list(self):
        report = self.engine.cluster_agents([])
        self.assertEqual(report.total_agents, 0)
        self.assertEqual(report.clusters_formed, 0)


if __name__ == "__main__":
    unittest.main()
