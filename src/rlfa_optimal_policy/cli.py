"""Command-line entry point for certificate generation and verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .counterexample import certificate_json, fraction_text, write_certificate
from .model import AuditInstance
from .n2 import characterize_n2
from .search import find_n2_counterexample


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rlfa-optimal")
    subparsers = parser.add_subparsers(dest="command", required=True)

    certificate = subparsers.add_parser("certificate", help="emit the exact JSON certificate")
    certificate.add_argument("--output", type=Path)

    verify = subparsers.add_parser("verify", help="compare a checked-in certificate to a fresh one")
    verify.add_argument(
        "path", type=Path, nargs="?", default=Path("certificates/counterexample.json")
    )

    search = subparsers.add_parser("search-n2", help="run the bounded exact rational search")
    search.add_argument("--max-denominator", type=int, default=6)

    characterize = subparsers.add_parser(
        "characterize-n2", help="solve an exact rational N=2 instance"
    )
    characterize.add_argument("--pi", nargs=2, default=("3/4", "1/4"))
    characterize.add_argument("--f", nargs=2, default=("1/3", "1"))
    characterize.add_argument("--epsilon", default="1/3")
    characterize.add_argument("--delta", default="1/20")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "certificate":
        if args.output:
            write_certificate(args.output)
        else:
            sys.stdout.write(certificate_json())
        return 0
    if args.command == "verify":
        expected = certificate_json()
        actual = args.path.read_text(encoding="utf-8")
        if actual != expected:
            sys.stderr.write(f"certificate mismatch: {args.path}\n")
            return 1
        print(f"verified exact certificate: {args.path}")
        return 0
    if args.command == "search-n2":
        hit = find_n2_counterexample(args.max_denominator)
        if hit is None:
            print("no counterexample found in the bounded grid")
            return 1
        print(
            "found N=2 counterexample: "
            f"pi={[fraction_text(x) for x in hit.instance.weights]}, "
            f"f={[fraction_text(x) for x in hit.instance.misstatements]}, "
            f"epsilon={fraction_text(hit.instance.epsilon)}, "
            f"E_oracle={fraction_text(hit.oracle_expectation)}, "
            f"E_propM={fraction_text(hit.alternative_expectation)}"
        )
        return 0
    if args.command == "characterize-n2":
        instance = AuditInstance.from_values(args.pi, args.f, args.epsilon, args.delta)
        result = characterize_n2(instance)
        record = {
            "N": 2,
            "pi": [fraction_text(value) for value in instance.weights],
            "f": [fraction_text(value) for value in instance.misstatements],
            "epsilon": fraction_text(instance.epsilon),
            "delta": fraction_text(instance.delta),
            "stopping_items_1_based": [index + 1 for index in result.stopping_items],
            "literal_simplex_optimum": fraction_text(result.optimal_value),
            "full_support_infimum": fraction_text(result.full_support_infimum),
            "full_support_attained": result.full_support_attained,
            "importance_support_infimum": fraction_text(
                result.importance_support_infimum
            ),
            "importance_support_attained": result.importance_support_attained,
            "oracle_defined": result.oracle_defined,
            "oracle_expected_tau": (
                fraction_text(result.oracle_expected_length)
                if result.oracle_expected_length is not None
                else None
            ),
            "oracle_is_globally_optimal": result.oracle_is_globally_optimal,
        }
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
