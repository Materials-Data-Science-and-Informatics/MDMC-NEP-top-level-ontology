"""
Download SKOS vocabulary from SKOSMOS.
"""

import requests
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone
import hashlib
import json


def download_skos(
    base_url: str = "https://matwerk.datamanager.kit.edu/skosmos",
    vocab_id: str = "prima",
    output_path: Optional[Path] = None,
    format: str = "rdf",
) -> tuple[bytes, dict]:
    """
    Download SKOS vocabulary from SKOSMOS.

    Args:
        base_url: Base URL of the SKOSMOS instance (without vocabulary path)
        vocab_id: Vocabulary ID (default: "prima")
        output_path: Optional path to save the downloaded RDF
        format: Output format ("rdf" for RDF/XML, "ttl" for Turtle)

    Returns:
        Tuple of (RDF content as bytes, metadata dict)

    Raises:
        requests.RequestException: If download fails
    """
    # SKOSMOS REST API endpoint for downloading vocabulary
    # Format: {base_url}/rest/v1/{vocab_id}/data?format={format_mime_type}
    url = f"{base_url}/rest/v1/{vocab_id}/data"
    
    # Map format to MIME type for the API
    format_mime_map = {
        "rdf": "application/rdf+xml",
        "ttl": "text/turtle",
    }
    format_mime = format_mime_map.get(format, "application/rdf+xml")
    
    params = {"format": format_mime}
    headers = {
        "Accept": format_mime,
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    content = response.content

    # Calculate checksum
    checksum = hashlib.sha256(content).hexdigest()

    # Extract metadata
    metadata = {
        "download_url": response.url,
        "download_timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "content_type": response.headers.get("Content-Type", ""),
        "content_length": len(content),
        "checksum_sha256": checksum,
        "format": format,
    }

    # Save to file if output_path is provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)

    return content, metadata


def save_snapshot(
    content: bytes,
    metadata: dict,
    snapshot_dir: Path,
    timestamp: Optional[datetime] = None,
) -> tuple[Path, Path]:
    """
    Save a snapshot of the SKOS vocabulary with metadata.

    Args:
        content: RDF content as bytes
        metadata: Metadata dictionary
        snapshot_dir: Directory to save snapshots
        timestamp: Optional timestamp (defaults to current time)

    Returns:
        Tuple of (RDF file path, metadata file path)
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    # Format timestamp as ISO 8601 without colons (for filesystem compatibility)
    timestamp_str = timestamp.strftime("%Y-%m-%dT%H-%M-%SZ")

    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Save RDF file
    rdf_path = snapshot_dir / f"{timestamp_str}.rdf"
    rdf_path.write_bytes(content)

    # Save metadata
    metadata_path = snapshot_dir / f"{timestamp_str}-metadata.json"
    snapshot_metadata = {
        **metadata,
        "snapshot_timestamp": timestamp.isoformat() + "Z",
        "rdf_file": rdf_path.name,
    }
    metadata_path.write_text(json.dumps(snapshot_metadata, indent=2))

    # Update latest symlink (if on Unix-like system)
    latest_path = snapshot_dir / "latest.rdf"
    try:
        if latest_path.exists() or latest_path.is_symlink():
            latest_path.unlink()
        latest_path.symlink_to(rdf_path.name)
    except (OSError, NotImplementedError):
        # Symlinks not supported (e.g., Windows without admin rights)
        # Just copy the file instead
        import shutil
        if latest_path.exists():
            latest_path.unlink()
        shutil.copy2(rdf_path, latest_path)

    return rdf_path, metadata_path

