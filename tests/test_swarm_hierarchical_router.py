"""
Unit tests for SwarmHierarchicalRouter.
"""

import unittest
from apex_swarm_orchestrator_kernel.core.models import AgentNode
from apex_swarm_orchestrator_kernel.core.swarm_hierarchical_router import (
    SwarmHierarchicalRouter,
)


class TestSwarmHierarchicalRouter(unittest.TestCase):
    def setUp(self):
        self.router = SwarmHierarchicalRouter(token_pruning_efficiency_pct=97.2)
        self.agents = [
            AgentNode(
                agent_id="dir_0",
                tier="TIER_0_DIRECTOR",
                domain="AI_COMPILERS",
                capability_vector=[0.99, 0.95, 0.99, 0.90, 0.98],
                rtt_ms=1.0,
                security_realm="REALM_ROOT",
                current_vram_gb=80.0,
                token_budget=1000000,
            ),
            AgentNode(
                agent_id="orch_compilers",
                tier="TIER_1_ORCHESTRATOR",
                domain="AI_COMPILERS",
                capability_vector=[0.95, 0.90, 0.94, 0.85, 0.96],
                rtt_ms=3.0,
                security_realm="REALM_ROOT",
                current_vram_gb=48.0,
                token_budget=500000,
            ),
            AgentNode(
                agent_id="lead_compilers",
                tier="TIER_2_LEADER",
                domain="AI_COMPILERS",
                capability_vector=[0.90, 0.92, 0.88, 0.80, 0.91],
                rtt_ms=6.0,
                security_realm="REALM_ROOT",
                current_vram_gb=32.0,
                token_budget=250000,
            ),
            AgentNode(
                agent_id="worker_tiler",
                tier="TIER_3_WORKER",
                domain="AI_COMPILERS",
                capability_vector=[0.75, 0.96, 0.82, 0.70, 0.80],
                rtt_ms=11.5,
                security_realm="REALM_ROOT",
                current_vram_gb=16.0,
                token_budget=100000,
            ),
        ]

    def test_hierarchical_mission_dispatch(self):
        report = self.router.route_mission(
            task_id="TASK_TILING_01",
            target_domain="AI_COMPILERS",
            agents=self.agents,
            raw_prompt_tokens=450_000,
        )

        self.assertEqual(report.origin_tier, "TIER_0_DIRECTOR")
        self.assertEqual(report.dispatched_tier, "TIER_3_WORKER")
        self.assertEqual(len(report.route_path), 4)
        self.assertLess(report.tokens_consumed, 15_000)  # Pruned from 450,000
        self.assertEqual(report.context_pruned_pct, 97.2)
        self.assertLess(report.total_latency_ms, 50.0)
        self.assertLess(report.solve_time_us, 5000.0)


if __name__ == "__main__":
    unittest.main()
