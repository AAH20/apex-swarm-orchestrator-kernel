"""
Field-Tailored Evaluation Metric Weights Arbiter for Autonomous Swarms.
Applies specialized weight tensors across five engineering domains:
1. Substation & Energy Grid Infrastructure
2. High-Frequency Trading & Market Making
3. Frontier AI Compilers & Silicon Tiling
4. Autonomous Cyber Defense & Zero-Trust
5. Spatial Intelligence & Swarm Robotics
Zero external pip dependencies. Pure Python 3.10+.
"""

from __future__ import annotations
import math
import time
from typing import List, Dict, Set, Tuple, Optional

from apex_swarm_orchestrator_kernel.core.models import (
    DomainWeightTensor,
    DomainEvaluationReport,
)

PRESET_DOMAIN_WEIGHTS: Dict[str, DomainWeightTensor] = {
    "GRID_INFRASTRUCTURE": DomainWeightTensor(
        domain_name="GRID_INFRASTRUCTURE",
        w_acc=0.30,
        w_lat=0.25,
        w_cost=0.05,
        w_safe=0.30,
        w_det=0.10,
        admission_threshold=0.90,
    ),
    "QUANT_FINANCE": DomainWeightTensor(
        domain_name="QUANT_FINANCE",
        w_acc=0.20,
        w_lat=0.45,
        w_cost=0.15,
        w_safe=0.10,
        w_det=0.10,
        admission_threshold=0.88,
    ),
    "AI_COMPILERS": DomainWeightTensor(
        domain_name="AI_COMPILERS",
        w_acc=0.35,
        w_lat=0.10,
        w_cost=0.15,
        w_safe=0.05,
        w_det=0.35,
        admission_threshold=0.90,
    ),
    "CYBER_DEFENSE": DomainWeightTensor(
        domain_name="CYBER_DEFENSE",
        w_acc=0.25,
        w_lat=0.20,
        w_cost=0.05,
        w_safe=0.30,
        w_det=0.20,
        admission_threshold=0.90,
    ),
    "SPATIAL_ROBOTICS": DomainWeightTensor(
        domain_name="SPATIAL_ROBOTICS",
        w_acc=0.25,
        w_lat=0.30,
        w_cost=0.10,
        w_safe=0.25,
        w_det=0.10,
        admission_threshold=0.87,
    ),
}


class DomainWeightsArbiter:
    """
    Sub-microsecond Field-Specific Swarm Evaluation Arbiter.
    Evaluates candidate swarm configurations against specialized multi-axis tensors.
    """

    def __init__(self, custom_tensors: Optional[Dict[str, DomainWeightTensor]] = None):
        self.tensors = custom_tensors or PRESET_DOMAIN_WEIGHTS

    def evaluate_candidate(
        self, domain_name: str, raw_metrics: Dict[str, float]
    ) -> DomainEvaluationReport:
        """
        Evaluates normalized candidate performance metrics against domain weights.
        raw_metrics should contain normalized [0.0, 1.0] keys:
        'accuracy', 'latency_score', 'cost_score', 'safety_score', 'determinism_score'
        """
        start_t = time.perf_counter()

        tensor = self.tensors.get(domain_name, PRESET_DOMAIN_WEIGHTS["GRID_INFRASTRUCTURE"])

        acc = raw_metrics.get("accuracy", 0.95)
        lat = raw_metrics.get("latency_score", 0.90)
        cost = raw_metrics.get("cost_score", 0.85)
        safe = raw_metrics.get("safety_score", 0.98)
        det = raw_metrics.get("determinism_score", 0.92)

        weighted_fitness = (
            (tensor.w_acc * acc)
            + (tensor.w_lat * lat)
            + (tensor.w_cost * cost)
            + (tensor.w_safe * safe)
            + (tensor.w_det * det)
        )

        admitted = weighted_fitness >= tensor.admission_threshold
        elapsed_us = (time.perf_counter() - start_t) * 1_000_000.0

        return DomainEvaluationReport(
            domain_name=domain_name,
            raw_metrics=raw_metrics,
            weighted_fitness=round(weighted_fitness, 4),
            admission_threshold=tensor.admission_threshold,
            admitted=admitted,
            eval_latency_us=round(elapsed_us, 2),
        )
