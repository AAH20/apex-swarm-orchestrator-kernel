"""
Unit tests for MAPElitesEvolutionPool.
"""

import unittest
from apex_swarm_orchestrator_kernel.core.models import AgentGenome
from apex_swarm_orchestrator_kernel.core.map_elites_evolution_pool import (
    MAPElitesEvolutionPool,
)


class TestMAPElitesEvolutionPool(unittest.TestCase):
    def setUp(self):
        self.pool = MAPElitesEvolutionPool(
            latency_bins=10, max_latency_ms=100.0, token_bins=10, max_tokens=10000
        )
        self.seeds = [
            AgentGenome(
                genome_id="seed_fast",
                prompt_template_id="tmpl_fast",
                tool_schema_ids=["tool_a", "tool_b"],
                temperature=0.1,
                reasoning_depth=2,
                cti_threshold_ms=150.0,
                latency_descriptor_ms=20.0,
                token_descriptor_count=2000,
            ),
            AgentGenome(
                genome_id="seed_deep",
                prompt_template_id="tmpl_deep",
                tool_schema_ids=["tool_c", "tool_d", "tool_e"],
                temperature=0.05,
                reasoning_depth=6,
                cti_threshold_ms=250.0,
                latency_descriptor_ms=60.0,
                token_descriptor_count=5000,
            ),
        ]

    def test_map_elites_evolution_cycle(self):
        report = self.pool.step_evolution(self.seeds, evaluations_per_cycle=25)

        self.assertEqual(report.total_evaluations, 25)
        self.assertGreater(report.archive_cells_filled, 0)
        self.assertGreater(report.archive_coverage_pct, 0.0)
        self.assertGreater(report.best_fitness, 0.0)
        self.assertLess(report.evolution_latency_us, 10000.0)


if __name__ == "__main__":
    unittest.main()
