"""Command-line entry point for certificate generation and verification."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .counterexample import certificate_json, fraction_text, write_certificate
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
    raise AssertionError("unreachable")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
