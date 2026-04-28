#!/usr/bin/env python3
"""AutoQ wrapper that initializes retry logic and logging before running.

This wrapper:
1. Sets up proper logging configuration
2. Initializes retry logic with exponential backoff
3. Runs AutoQ with the provided arguments
"""

import logging
import sys
import os

# Configure logging BEFORE importing benchmark_qed modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set specific loggers
logging.getLogger('benchmark_qed').setLevel(logging.INFO)
logging.getLogger('benchmark_qed.llm.retry_wrapper').setLevel(logging.INFO)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

log = logging.getLogger(__name__)


def main():
    """Initialize retry logic and run AutoQ."""
    log.info("Initializing retry logic and logging...")
    
    # Import and initialize retry wrapper
    try:
        from benchmark_qed.llm.retry_wrapper import init_retry_and_logging
        init_retry_and_logging()
        log.info("Retry logic initialized successfully")
    except ImportError as e:
        log.warning(f"Could not import retry wrapper: {e}")
        log.warning("Continuing without retry logic...")
    
    # Import AutoQ CLI
    from benchmark_qed.autoq.cli import app
    
    # Inject 'autoq' command as first arg (Typer CLI expects subcommand)
    # Original args: [config_path, output_dir]
    # Need: ['autoq', config_path, output_dir, --generation-types, ...]
    args = sys.argv[1:]
    
    # Get generation types from env var (default: data_local,data_global only)
    # This avoids activity questions which generate many more queries
    gen_types_env = os.environ.get('GENERATION_TYPES', 'data_local,data_global')
    gen_types = [gt.strip() for gt in gen_types_env.split(',') if gt.strip()]
    
    # Validate generation types
    VALID_TYPES = {'data_local', 'data_global', 'data_linked', 'activity_local', 'activity_global'}
    invalid_types = [gt for gt in gen_types if gt not in VALID_TYPES]
    if invalid_types:
        log.error(f"Invalid GENERATION_TYPES: {invalid_types}")
        log.error(f"Valid types are: {sorted(VALID_TYPES)}")
        sys.exit(1)
    
    if not gen_types:
        log.error("GENERATION_TYPES cannot be empty")
        sys.exit(1)
    
    # Build generation-types args
    gen_type_args = []
    for gt in gen_types:
        gen_type_args.extend(['--generation-types', gt])
    
    log.info(f"Running AutoQ with args: {args}")
    log.info(f"Generation types: {gen_types}")
    
    # Modify sys.argv for Typer
    sys.argv = [sys.argv[0], 'autoq'] + args + gen_type_args
    
    # Run AutoQ
    sys.exit(app())


if __name__ == "__main__":
    main()
