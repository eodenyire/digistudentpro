#!/bin/bash
# Quick test runner script
# Usage: bash run_tests.sh

echo "========================================================================"
echo "                   🚀 DIGISTUDENTPRO TEST SUITE 🚀"
echo "========================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run Python test runner
python3 run_all_tests.py

echo ""
echo "========================================================================"
echo "Test suite execution completed!"
echo "========================================================================"
