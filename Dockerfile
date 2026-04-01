# BenchmarkQED Container Image
# For running AutoQ, AutoE, AutoD and LGR Search as containerized services

# Azure Linux 3.0 base - SFI compliant, fewer CVEs than Debian
FROM mcr.microsoft.com/azurelinux/base/python:3

# Install system dependencies (no azcopy - using Azure SDK instead for SFI compliance)
# Azure Linux uses tdnf instead of apt-get
RUN tdnf install -y \
    git \
    curl \
    gettext \
    tar \
    ca-certificates \
    && tdnf upgrade -y python3 python3-libs libarchive nghttp2 \
    && tdnf clean all

# Set working directory
WORKDIR /app

# Install uv directly from GitHub releases (latest binary with security fixes)
RUN curl -sL https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar xz --strip-components=1 -C /usr/bin \
    && chmod +x /usr/bin/uv /usr/bin/uvx

# Copy dependency files first (for caching)
COPY pyproject.toml ./
COPY README.md ./

# Copy the benchmark_qed package and .git for dynamic versioning
COPY benchmark_qed/ ./benchmark_qed/
COPY .git/ ./.git/

# Install the package (requires .git for uv-dynamic-versioning)
RUN pip install --no-cache-dir . azure-storage-queue azure-identity

# SFI CVE Fixes: MUST be AFTER main install to override transitive dependencies
# CVE-2026-1703 (pip), CVE-2026-24049 (wheel), CVE-2026-23949 (jaraco.context)
# CVE-2026-32597 (PyJWT), CVE-2026-34073/CVE-2026-26007 (cryptography), CVE-2026-25645 (requests)
# CVE-2025-66418/CVE-2025-66471/CVE-2026-21441 (urllib3), CVE-2025-69223-69230/CVE-2025-53643 (aiohttp)
# CVE-2026-21226 (azure-core), CVE-2025-66034 (fonttools), CVE-2026-25990 (pillow), CVE-2026-4539 (pygments)
# Use --ignore-installed because Azure Linux has system-managed pip/wheel via RPM
RUN pip install --no-cache-dir --ignore-installed \
    "pip>=26.0" "wheel>=0.46.2" "jaraco.context>=6.1.0" \
    "PyJWT>=2.12.0" \
    "cryptography>=46.0.6" \
    "requests>=2.33.0" \
    "urllib3>=2.6.3" \
    "aiohttp>=3.13.3" \
    "azure-core>=1.38.0" \
    "fonttools>=4.60.2" \
    "pillow>=12.1.1" \
    "pygments>=2.20.0"

# Remove .git after install (not needed at runtime, reduces image size)
RUN rm -rf .git

# Create directories for data and config
RUN mkdir -p /data/input /data/output /config

# Copy default settings template (will be overwritten by mount)
COPY settings.template.yaml /config/settings.yaml

# Environment variables for Azure authentication
ENV AZURE_CLIENT_ID=""
ENV AZURE_TENANT_ID=""

# Environment variables for LGR Queue Search (configurable per bookshelf instance)
ENV LGR_STORAGE_ACCOUNT="stdbksfyjp4laaaaa"
ENV LGR_IN_QUEUE="bksidentitytestnew-mykb-v1-in"
ENV LGR_OUT_QUEUE="bksidentitytestnew-mykb-v1-out"
ENV LGR_POLL_INTERVAL="30"
ENV LGR_TIMEOUT="20"

# Environment variables for blob input (same pattern as lgr-app)
ENV BLOB_INPUT_URL=""
ENV BLOB_OUTPUT_URL=""

# Copy startup script and blob download helper
COPY scripts/startup.sh /app/startup.sh
COPY scripts/run-eval.sh /app/run-eval.sh
COPY scripts/run_autoq.py /app/scripts/run_autoq.py
COPY scripts/export_qa_to_pdf.py /app/scripts/export_qa_to_pdf.py
COPY scripts/blob_download.py /app/scripts/blob_download.py
RUN chmod +x /app/startup.sh /app/run-eval.sh

# Default entrypoint runs startup script (downloads data, then runs command)
ENTRYPOINT ["/app/startup.sh"]
CMD ["benchmark-qed", "--help"]

# Labels for SFI compliance
LABEL org.opencontainers.image.title="BenchmarkQED"
LABEL org.opencontainers.image.description="Automated benchmarking of RAG systems with LGR integration"
LABEL org.opencontainers.image.source="https://github.com/microsoft/benchmark-qed"
LABEL com.microsoft.security.scan-required="true"
