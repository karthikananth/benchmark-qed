# BenchmarkQED Container Image
# For running AutoQ, AutoE, AutoD and LGR Search as containerized services

# Azure Linux 3.0 base - SFI compliant, fewer CVEs than Debian
FROM mcr.microsoft.com/azurelinux/base/python:3

# Install system dependencies + azcopy for fast blob downloads
# Azure Linux uses tdnf instead of apt-get
# azcopy installed via tdnf (official Microsoft package, maintained)
RUN tdnf install -y \
    git \
    curl \
    gettext \
    tar \
    ca-certificates \
    azcopy \
    && tdnf upgrade -y libarchive nghttp2 \
    && tdnf clean all

# Set working directory
WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

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
# Use --ignore-installed because Azure Linux has system-managed pip/wheel via RPM
RUN pip install --no-cache-dir --ignore-installed "pip>=26.0" "wheel>=0.46.2" "jaraco.context>=6.1.0"

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

# Copy startup script
COPY scripts/startup.sh /app/startup.sh
COPY scripts/run-eval.sh /app/run-eval.sh
COPY scripts/run_autoq.py /app/scripts/run_autoq.py
COPY scripts/export_qa_to_pdf.py /app/scripts/export_qa_to_pdf.py
RUN chmod +x /app/startup.sh /app/run-eval.sh

# Default entrypoint runs startup script (downloads data, then runs command)
ENTRYPOINT ["/app/startup.sh"]
CMD ["benchmark-qed", "--help"]

# Labels for SFI compliance
LABEL org.opencontainers.image.title="BenchmarkQED"
LABEL org.opencontainers.image.description="Automated benchmarking of RAG systems with LGR integration"
LABEL org.opencontainers.image.source="https://github.com/microsoft/benchmark-qed"
LABEL com.microsoft.security.scan-required="true"
