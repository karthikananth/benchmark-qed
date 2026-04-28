#!/usr/bin/env python3
"""
Blob Download Script - Replaces azcopy for SFI compliance
Downloads blobs from Azure Storage using azure-storage-blob SDK with managed identity.
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, ContainerClient


def parse_blob_url(url: str) -> tuple[str, str, str]:
    """Parse blob URL into account, container, and prefix."""
    # Handle URLs like: https://account.blob.core.windows.net/container/path
    parsed = urlparse(url)
    account = parsed.netloc.split('.')[0]
    path_parts = parsed.path.strip('/').split('/', 1)
    container = path_parts[0]
    prefix = path_parts[1] if len(path_parts) > 1 else ""
    return account, container, prefix


def get_credential():
    """Get Azure credential - prefer managed identity if client ID is set."""
    client_id = os.environ.get("AZURE_CLIENT_ID")
    if client_id:
        print(f"      Using managed identity: {client_id[:8]}...")
        return ManagedIdentityCredential(client_id=client_id)
    else:
        print("      Using DefaultAzureCredential")
        return DefaultAzureCredential()


def download_blob(container_client: ContainerClient, blob_name: str, target_dir: Path) -> str:
    """Download a single blob to target directory."""
    target_path = target_dir / blob_name
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    blob_client = container_client.get_blob_client(blob_name)
    with open(target_path, "wb") as f:
        stream = blob_client.download_blob()
        f.write(stream.readall())
    
    return blob_name


def download_blobs(blob_url: str, target_dir: str, max_workers: int = 8) -> int:
    """Download all blobs from URL to target directory."""
    account, container, prefix = parse_blob_url(blob_url)
    target_path = Path(target_dir)
    
    print(f"      Account: {account}")
    print(f"      Container: {container}")
    print(f"      Prefix: {prefix or '(root)'}")
    
    # Create blob service client
    account_url = f"https://{account}.blob.core.windows.net"
    credential = get_credential()
    blob_service = BlobServiceClient(account_url, credential=credential)
    container_client = blob_service.get_container_client(container)
    
    # List all blobs with prefix
    blobs = list(container_client.list_blobs(name_starts_with=prefix))
    total = len(blobs)
    print(f"      Found {total} blobs to download")
    
    if total == 0:
        return 0
    
    # Download in parallel
    downloaded = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_blob, container_client, blob.name, target_path): blob.name
            for blob in blobs
        }
        
        for future in as_completed(futures):
            blob_name = futures[future]
            try:
                future.result()
                downloaded += 1
                if downloaded % 10 == 0 or downloaded == total:
                    print(f"      Progress: {downloaded}/{total} blobs")
            except Exception as e:
                failed += 1
                print(f"      ERROR downloading {blob_name}: {e}")
    
    if failed > 0:
        print(f"      WARNING: {failed} blobs failed to download")
        return -1
    
    return downloaded


def main():
    if len(sys.argv) < 3:
        print("Usage: blob_download.py <blob_url> <target_dir>")
        sys.exit(1)
    
    blob_url = sys.argv[1]
    target_dir = sys.argv[2]
    
    start_time = time.time()
    count = download_blobs(blob_url, target_dir)
    elapsed = time.time() - start_time
    
    if count < 0:
        print(f"      Download completed with errors in {elapsed:.1f} seconds")
        sys.exit(1)
    else:
        print(f"      Downloaded {count} files in {elapsed:.1f} seconds")
        sys.exit(0)


if __name__ == "__main__":
    main()
