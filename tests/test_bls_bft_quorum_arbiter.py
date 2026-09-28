"""
Unit tests for BLSBFTQuorumArbiter.
"""

import unittest
from apex_swarm_orchestrator_kernel.core.models import BLSQuorumVote
from apex_swarm_orchestrator_kernel.core.bls_bft_quorum_arbiter import (
    BLSBFTQuorumArbiter,
)


class TestBLSBFTQuorumArbiter(unittest.TestCase):
    def setUp(self):
        self.arbiter = BLSBFTQuorumArbiter(quorum_threshold_pct=0.67)

    def test_bft_quorum_with_byzantine_fault_filtering(self):
        payload = "DISPATCH_PROTECTIVE_TRIP_FEEDER_01"
        votes = [
            BLSQuorumVote("voter_1", payload, "sig_1", 1.0, False),
            BLSQuorumVote("voter_2", payload, "sig_2", 1.0, False),
            BLSQuorumVote("voter_3", payload, "sig_3", 1.0, False),
            BLSQuorumVote("voter_4_adversary", "TAMPERED_PAYLOAD", "sig_4", 1.0, True),
            BLSQuorumVote("voter_5", payload, "sig_5", 1.0, False),
        ]
        report = self.arbiter.verify_and_aggregate_quorum(votes, payload)

        self.assertEqual(report.total_voters, 5)
        self.assertEqual(report.byzantine_faults_tolerated, 1)
        self.assertTrue(report.quorum_reached)
        self.assertTrue(report.aggregated_signature.startswith("bls_agg_proof_"))
        self.assertLess(report.quorum_latency_us, 5000.0)

    def test_insufficient_weight_fails_quorum(self):
        payload = "EXECUTE_SHUTDOWN"
        votes = [
            BLSQuorumVote("voter_1", payload, "sig_1", 1.0, False),
            BLSQuorumVote("voter_2", payload, "sig_2", 1.0, True),  # Faulty
            BLSQuorumVote("voter_3", payload, "sig_3", 1.0, True),  # Faulty
        ]
        report = self.arbiter.verify_and_aggregate_quorum(votes, payload)
        self.assertFalse(report.quorum_reached)
        self.assertEqual(report.aggregated_signature, "QUORUM_NOT_REACHED")


if __name__ == "__main__":
    unittest.main()
