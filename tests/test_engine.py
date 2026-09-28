"""
Unit tests for ApexSwarmOrchestratorEngine and synthetic state generator.
"""

import unittest
from apex_swarm_orchestrator_kernel.engine import (
    ApexSwarmOrchestratorEngine,
    generate_synthetic_swarm_state,
)


class TestApexSwarmOrchestratorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ApexSwarmOrchestratorEngine()
        (
            self.agents,
            self.genomes,
            self.metrics,
            self.votes,
            self.task_id,
        ) = generate_synthetic_swarm_state()

    def test_synthetic_state_integrity(self):
        self.assertGreater(len(self.agents), 15)
        self.assertGreater(len(self.genomes), 0)
        self.assertGreater(len(self.metrics), 0)
        self.assertGreater(len(self.votes), 0)
        self.assertIsNotNone(self.task_id)

    def test_engine_subsystem_execution(self):
        # 1. Spectral Clustering
        rep_cluster = self.engine.cluster_and_elect_leaders(self.agents, 5)
        self.assertGreater(rep_cluster.clusters_formed, 0)
        self.assertEqual(len(rep_cluster.leader_assignments), rep_cluster.clusters_formed)

        # 2. MAP-Elites Evolution
        rep_evo = self.engine.step_map_elites_evolution(self.genomes, 20)
        self.assertGreater(rep_evo.archive_cells_filled, 0)
        self.assertGreater(rep_evo.best_fitness, 0.0)

        # 3. Domain Weights Arbiter
        rep_eval = self.engine.evaluate_domain_weights("GRID_INFRASTRUCTURE", self.metrics)
        self.assertTrue(rep_eval.admitted)
        self.assertGreaterEqual(rep_eval.weighted_fitness, rep_eval.admission_threshold)

        # 4. BLS BFT Quorum
        rep_quorum = self.engine.verify_bft_quorum(self.votes, "ACTUATE_DVFS_SHED_250MW")
        self.assertTrue(rep_quorum.quorum_reached)
        self.assertEqual(rep_quorum.byzantine_faults_tolerated, 1)

        # 5. Hierarchical Routing
        rep_route = self.engine.route_hierarchical_mission(self.task_id, "GRID_INFRASTRUCTURE", self.agents)
        self.assertEqual(rep_route.origin_tier, "TIER_0_DIRECTOR")
        self.assertEqual(rep_route.dispatched_tier, "TIER_3_WORKER")
        self.assertLess(rep_route.tokens_consumed, 15_000)

    def test_full_pipeline_benchmark(self):
        bench_rep = self.engine.run_full_pipeline_benchmark(iterations=10)
        self.assertGreater(bench_rep.total_runtime_ms, 0.0)
        self.assertTrue(hasattr(bench_rep, "spectral_clustering_summary"))
        self.assertTrue(hasattr(bench_rep, "map_elites_evolution_summary"))
        self.assertTrue(hasattr(bench_rep, "domain_evaluation_summary"))
        self.assertTrue(hasattr(bench_rep, "bft_quorum_summary"))
        self.assertTrue(hasattr(bench_rep, "hierarchical_routing_summary"))


if __name__ == "__main__":
    unittest.main()
