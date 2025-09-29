#!/bin/bash
# Cleanup duplicate pipeline files

echo "Removing backup/duplicate files..."

# Remove BACKUP files
rm -f pipeline/*_BACKUP.py
rm -f pipeline/*_FIXED.py
rm -f pipeline/*_FIXED2.py
rm -f pipeline/*_COMPLETE.py
rm -f pipeline/*_CONNECTED.py
rm -f pipeline/*_WORKING.py
rm -f pipeline/*_REAL.py
rm -f pipeline/*_STREAMING.py
rm -f pipeline/*_with_quotes.py

# Remove duplicate sp500 fetchers
rm -f pipeline/00a_get_sp500.py
rm -f pipeline/00a_get_sp500_fixed.py

# Keep only the live version
echo "✅ Cleaned up duplicates"

# Show remaining files
echo ""
echo "Remaining pipeline files:"
ls -1 pipeline/*.py | wc -l
echo "files"
