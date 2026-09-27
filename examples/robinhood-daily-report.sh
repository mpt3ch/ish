#!/bin/sh
# Example: Daily Portfolio Report
# This script can be run daily to check your portfolio and specific stocks

# Make sure you're logged in first:
# robinhood-cli login

echo "========================================="
echo "   Daily Portfolio & Market Report"
echo "========================================="
echo ""

# Display portfolio summary
echo "YOUR PORTFOLIO"
echo "-----------------------------------------"
robinhood-cli portfolio
echo ""

# Display specific stock quotes
echo "MARKET DATA - YOUR WATCHLIST"
echo "-----------------------------------------"
echo ""
echo "Apple Inc. (AAPL):"
robinhood-cli quote AAPL
echo ""

echo "Microsoft Corp. (MSFT):"
robinhood-cli quote MSFT
echo ""

echo "Google (GOOGL):"
robinhood-cli quote GOOGL
echo ""

echo "Recent Orders"
echo "-----------------------------------------"
robinhood-cli orders
echo ""
echo "========================================="
