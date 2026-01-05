"""
Command-line interface for PRIMA SKOS Monitor.
"""

import argparse
import sys
from pathlib import Path

# Automatically add monitor_utils to Python path if not already there
# This allows running without PYTHONPATH=monitor_utils
_cli_file = Path(__file__).resolve()
_monitor_utils_dir = _cli_file.parent.parent.parent
if str(_monitor_utils_dir) not in sys.path:
    sys.path.insert(0, str(_monitor_utils_dir))

from datetime import datetime, timezone
from prima_skos_monitor.downloader import download_skos, save_snapshot
from prima_skos_monitor.analyzer import parse_skos, load_skos_from_file
from prima_skos_monitor.comparator import compare_versions
from prima_skos_monitor.reporter import generate_report


def cmd_download(args):
    """Download SKOS vocabulary from SKOSMOS."""
    print(f"Downloading PRIMA SKOS from {args.base_url}...")
    try:
        content, metadata = download_skos(
            base_url=args.base_url,
            vocab_id=args.vocab_id,
            format=args.format,
        )

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(content)
            print(f"✓ Downloaded {len(content)} bytes to {output_path}")
        else:
            print(f"✓ Downloaded {len(content)} bytes")

        print(f"  Checksum: {metadata['checksum_sha256']}")
        print(f"  Content-Type: {metadata['content_type']}")

        if args.save_snapshot:
            snapshot_dir = Path(args.snapshot_dir)
            rdf_path, metadata_path = save_snapshot(
                content, metadata, snapshot_dir, timestamp=datetime.now(timezone.utc)
            )
            print(f"✓ Saved snapshot: {rdf_path}")
            print(f"✓ Saved metadata: {metadata_path}")

    except Exception as e:
        print(f"✗ Error downloading SKOS: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_compare(args):
    """Compare two SKOS versions."""
    print("Loading baseline version...")
    baseline_path = Path(args.baseline)
    if not baseline_path.exists():
        print(f"✗ Baseline file not found: {baseline_path}", file=sys.stderr)
        sys.exit(1)

    baseline_format = "xml" if baseline_path.suffix == ".rdf" else "turtle"
    baseline_concepts = load_skos_from_file(baseline_path, format=baseline_format)
    print(f"✓ Loaded {len(baseline_concepts)} concepts from baseline")

    print("Loading new version...")
    if args.new:
        new_path = Path(args.new)
        if not new_path.exists():
            print(f"✗ New version file not found: {new_path}", file=sys.stderr)
            sys.exit(1)
        new_format = "xml" if new_path.suffix == ".rdf" else "turtle"
        new_concepts = load_skos_from_file(new_path, format=new_format)
    else:
        # Download new version
        print("Downloading latest version from SKOSMOS...")
        content, _ = download_skos(
            base_url=args.base_url,
            vocab_id=args.vocab_id,
            format=args.format,
        )
        new_concepts = parse_skos(content, format=args.format)

    print(f"✓ Loaded {len(new_concepts)} concepts from new version")

    print("Comparing versions...")
    report = compare_versions(baseline_concepts, new_concepts)

    if not report.has_changes():
        print("✓ No changes detected")
    else:
        summary = report.get_summary()
        print(f"✗ Changes detected:")
        print(f"  - New concepts: {summary['new_concepts']}")
        print(f"  - Deleted concepts: {summary['deleted_concepts']}")
        print(f"  - Modified concepts: {summary['modified_concepts']}")

    if args.output:
        output_path = Path(args.output)
        report_text = generate_report(
            report,
            baseline_concepts=baseline_concepts,
            new_concepts=new_concepts,
            output_path=output_path,
        )
        print(f"✓ Report saved to {output_path}")
    else:
        report_text = generate_report(
            report,
            baseline_concepts=baseline_concepts,
            new_concepts=new_concepts,
        )
        print("\n" + "=" * 80)
        print(report_text)

    return report


def cmd_report(args):
    """Generate a report from a comparison."""
    # This is essentially the same as compare, but we assume comparison was already done
    print("This command requires a comparison result.")
    print("Use 'compare' command instead, or provide comparison data.")
    sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PRIMA SKOS Monitor - Track changes in PRIMA SKOS vocabulary"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download SKOS vocabulary")
    download_parser.add_argument(
        "--base-url",
        default="https://matwerk.datamanager.kit.edu/skosmos",
        help="SKOSMOS base URL (without vocabulary path)",
    )
    download_parser.add_argument(
        "--vocab-id", default="prima", help="Vocabulary ID"
    )
    download_parser.add_argument(
        "--format", default="rdf", choices=["rdf", "ttl"], help="Output format"
    )
    download_parser.add_argument(
        "-o", "--output", help="Output file path"
    )
    download_parser.add_argument(
        "--save-snapshot",
        action="store_true",
        help="Save as timestamped snapshot",
    )
    download_parser.add_argument(
        "--snapshot-dir",
        default="monitor_utils/skos_snapshots",
        help="Directory for snapshots",
    )
    download_parser.set_defaults(func=cmd_download)

    # Compare command
    compare_parser = subparsers.add_parser(
        "compare", help="Compare two SKOS versions"
    )
    compare_parser.add_argument(
        "--baseline",
        required=True,
        help="Baseline RDF file path",
    )
    compare_parser.add_argument(
        "--new",
        help="New version RDF file path (if not provided, downloads from SKOSMOS)",
    )
    compare_parser.add_argument(
        "--base-url",
        default="https://matwerk.datamanager.kit.edu/skosmos",
        help="SKOSMOS base URL (without vocabulary path, used if --new not provided)",
    )
    compare_parser.add_argument(
        "--vocab-id", default="prima", help="Vocabulary ID"
    )
    compare_parser.add_argument(
        "--format", default="rdf", choices=["rdf", "ttl"], help="RDF format"
    )
    compare_parser.add_argument(
        "-o", "--output", help="Output report file path"
    )
    compare_parser.set_defaults(func=cmd_compare)

    # Report command (for future use)
    report_parser = subparsers.add_parser(
        "report", help="Generate change report (use 'compare' instead)"
    )
    report_parser.set_defaults(func=cmd_report)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()

