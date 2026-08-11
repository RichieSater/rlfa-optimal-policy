"""Exact tools for optimal sampling in risk-limiting financial audits."""

from .approxkelly import ApproxKellyConfig, evaluate_policy, solve_action_mesh
from .confidence import ReleasedApproxKellyLogicalN2
from .counterexample import COUNTEREXAMPLE, build_certificate
from .dp import enumerate_terminal_paths, expected_audit_length
from .industry_certificate import build_industry_certificate
from .logical import fixed_risk_oracle_gap_family, solve_logical_unit_cost
from .model import AuditInstance, Interval
from .n2 import N2Characterization, characterize_n2, stopping_items
from .policies import (
    FixedFirstDistributionPolicy,
    FixedPriorityPolicy,
    MeshPriorityPolicy,
    OracleContributionPolicy,
    ProportionalMonetaryScorePolicy,
    ProportionalValuePolicy,
)
from .robust import BoxAuditProblem, multiplicative_score_box, solve_box_costs, solve_box_unit_cost

__all__ = [
    "ApproxKellyConfig",
    "AuditInstance",
    "BoxAuditProblem",
    "COUNTEREXAMPLE",
    "FixedFirstDistributionPolicy",
    "FixedPriorityPolicy",
    "Interval",
    "MeshPriorityPolicy",
    "N2Characterization",
    "OracleContributionPolicy",
    "ProportionalMonetaryScorePolicy",
    "ProportionalValuePolicy",
    "ReleasedApproxKellyLogicalN2",
    "build_certificate",
    "build_industry_certificate",
    "characterize_n2",
    "enumerate_terminal_paths",
    "evaluate_policy",
    "expected_audit_length",
    "fixed_risk_oracle_gap_family",
    "multiplicative_score_box",
    "solve_action_mesh",
    "solve_box_costs",
    "solve_box_unit_cost",
    "solve_logical_unit_cost",
    "stopping_items",
]
