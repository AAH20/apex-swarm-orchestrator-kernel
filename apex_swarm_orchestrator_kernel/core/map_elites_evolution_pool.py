"""
MAP-Elites Quality-Diversity Evolutionary Archive for Autonomous Swarm Agents.
Maintains a 2D feature grid (Latency vs Token Consumption) storing Pareto-optimal
agent genomes. Evaluates multi-objective fitness and drives stochastic prompt/tool mutation.
Zero external pip dependencies. Pure Python 3.10+.
"""

from __future__ import annotations
import math
import random
import time
from typing import List, Dict, Set, Tuple, Optional

from apex_swarm_orchestrator_kernel.core.models import (
    AgentGenome,
    MAPElitesArchiveReport,
)


class MAPElitesEvolutionPool:
    """
    Sub-millisecond Quality-Diversity Archive & Mutation Engine.
    Evolves agent populations across continuous behavioral dimensions rather than converging
    to brittle local optima.
    """

    def __init__(
        self,
        latency_bins: int = 10,
        max_latency_ms: float = 100.0,
        token_bins: int = 10,
        max_tokens: int = 10000,
    ):
        self.latency_bins = latency_bins
        self.max_latency_ms = max_latency_ms
        self.token_bins = token_bins
        self.max_tokens = max_tokens
        # Archive maps (bin_lat, bin_tok) -> AgentGenome
        self.archive: Dict[Tuple[int, int], AgentGenome] = {}

    def get_feature_coordinates(self, latency_ms: float, tokens: int) -> Tuple[int, int]:
        """Maps continuous descriptors into discrete 2D grid coordinates."""
        lat_bin = min(
            self.latency_bins - 1,
            max(0, int((latency_ms / self.max_latency_ms) * self.latency_bins)),
        )
        tok_bin = min(
            self.token_bins - 1,
            max(0, int((tokens / self.max_tokens) * self.token_bins)),
        )
        return (lat_bin, tok_bin)

    def evaluate_fitness(
        self, genome: AgentGenome, accuracy: float, latency_ms: float, tokens: int
    ) -> float:
        """Computes multi-objective Pareto fitness score [0.0, 1.0]."""
        lat_norm = max(0.0, 1.0 - (latency_ms / self.max_latency_ms))
        tok_norm = max(0.0, 1.0 - (tokens / self.max_tokens))
        # 50% accuracy, 25% latency efficiency, 25% token frugality
        return (0.50 * accuracy) + (0.25 * lat_norm) + (0.25 * tok_norm)

    def mutate_genome(self, parent: AgentGenome, generation_id: int) -> AgentGenome:
        """Generates child genome with stochastic mutations to prompt, tools, and depth."""
        new_temp = round(min(1.0, max(0.0, parent.temperature + random.uniform(-0.08, 0.08))), 2)
        new_depth = max(1, min(12, parent.reasoning_depth + random.choice([-1, 0, 1])))
        new_cti = max(50.0, min(500.0, parent.cti_threshold_ms + random.uniform(-25.0, 25.0)))

        tools = list(parent.tool_schema_ids)
        if random.random() < 0.20 and len(tools) > 1:
            tools.pop(random.randint(0, len(tools) - 1))
        elif random.random() < 0.20 and len(tools) < 8:
            tools.append(f"tool_schema_ext_{len(tools):02d}")

        return AgentGenome(
            genome_id=f"child_gen{generation_id}_{random.randint(1000, 9999)}",
            prompt_template_id=parent.prompt_template_id,
            tool_schema_ids=tools,
            temperature=new_temp,
            reasoning_depth=new_depth,
            cti_threshold_ms=round(new_cti, 1),
        )

    def step_evolution(
        self,
        seed_population: List[AgentGenome],
        evaluations_per_cycle: int = 50,
    ) -> MAPElitesArchiveReport:
        """
        Executes evolutionary mutation and insertion into the quality-diversity archive.
        """
        start_t = time.perf_counter()

        # Seed archive with initial population
        for g in seed_population:
            coords = self.get_feature_coordinates(g.latency_descriptor_ms, g.token_descriptor_count)
            if coords not in self.archive or g.fitness_score > self.archive[coords].fitness_score:
                self.archive[coords] = g

        parents = list(self.archive.values())
        if not parents:
            parents = seed_population

        eval_count = 0
        for i in range(evaluations_per_cycle):
            parent = random.choice(parents)
            child = self.mutate_genome(parent, i)

            # Simulated performance evaluation
            sim_acc = min(0.999, max(0.70, 0.85 + (child.reasoning_depth * 0.015) - (child.temperature * 0.05)))
            sim_lat = min(self.max_latency_ms, max(2.0, 15.0 + (child.reasoning_depth * 4.5) + len(child.tool_schema_ids) * 2.0))
            sim_tok = min(self.max_tokens, max(200, 1200 + child.reasoning_depth * 350 + len(child.tool_schema_ids) * 150))

            fitness = self.evaluate_fitness(child, sim_acc, sim_lat, sim_tok)
            child.fitness_score = round(fitness, 4)
            child.latency_descriptor_ms = round(sim_lat, 2)
            child.token_descriptor_count = int(sim_tok)

            coords = self.get_feature_coordinates(sim_lat, sim_tok)
            if coords not in self.archive or fitness > self.archive[coords].fitness_score:
                self.archive[coords] = child
                parents.append(child)

            eval_count += 1

        total_cells = self.latency_bins * self.token_bins
        cells_filled = len(self.archive)
        coverage_pct = (cells_filled / max(1, total_cells)) * 100.0
        best_fit = max((g.fitness_score for g in self.archive.values()), default=0.0)

        elapsed_us = (time.perf_counter() - start_t) * 1_000_000.0

        return MAPElitesArchiveReport(
            total_evaluations=eval_count,
            archive_cells_filled=cells_filled,
            archive_coverage_pct=round(coverage_pct, 2),
            best_fitness=round(best_fit, 4),
            pareto_frontier_count=cells_filled,
            evolution_latency_us=round(elapsed_us, 2),
        )
