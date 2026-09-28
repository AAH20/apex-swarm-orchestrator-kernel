"""
Unit tests for DomainWeightsArbiter.
"""

import unittest
from apex_swarm_orchestrator_kernel.core.domain_weights_arbiter import (
    DomainWeightsArbiter,
    PRESET_DOMAIN_WEIGHTS,
)


class TestDomainWeightsArbiter(unittest.TestCase):
    def setUp(self):
        self.arbiter = DomainWeightsArbiter()

    def test_grid_infrastructure_admission(self):
        high_safety_metrics = {
            "accuracy": 0.98,
            "latency_score": 0.95,
            "cost_score": 0.80,
            "safety_score": 0.99,
            "determinism_score": 0.95,
        }
        report = self.arbiter.evaluate_candidate("GRID_INFRASTRUCTURE", high_safety_metrics)
        self.assertTrue(report.admitted)
        self.assertGreaterEqual(report.weighted_fitness, report.admission_threshold)
        self.assertLess(report.eval_latency_us, 5000.0)

    def test_quant_finance_low_latency_requirement(self):
        slow_candidate_metrics = {
            "accuracy": 0.99,
            "latency_score": 0.50,  # Slow latency severely penalizes Quant Finance
            "cost_score": 0.95,
            "safety_score": 0.95,
            "determinism_score": 0.95,
        }
        report = self.arbiter.evaluate_candidate("QUANT_FINANCE", slow_candidate_metrics)
        self.assertFalse(report.admitted)
        self.assertLess(report.weighted_fitness, report.admission_threshold)


if __name__ == "__main__":
    unittest.main()
