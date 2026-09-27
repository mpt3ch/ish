#!/bin/sh
# Example: Trading Automation Script
# This demonstrates how to use robinhood-cli in automated workflows

# Simple portfolio rebalancing check
check_portfolio_balance() {
    echo "Checking portfolio balance..."
    # Get portfolio and check if any position is more than 50% of total
    robinhood-cli portfolio
}

# Alert on price changes
check_price_alerts() {
    local symbol=$1
    local alert_price=$2
    
    # This is a simplified example
    # In practice, you'd parse the output and compare values
    echo "Checking price alert for $symbol at \$$alert_price"
    robinhood-cli quote "$symbol"
}

# Example: Buy dips strategy
# Only execute if you understand the risks!
buy_dips_example() {
    local symbol=$1
    local target_price=$2
    local quantity=$3
    
    echo "Example: Would buy $quantity shares of $symbol at $target_price"
    # Uncomment to actually execute (use with caution!):
    # robinhood-cli buy "$symbol" "$quantity" --price "$target_price"
}

# Main execution
echo "========================================="
echo "   Trading Automation Example"
echo "========================================="
echo ""

# Check your portfolio
check_portfolio_balance
echo ""

# Check some prices
check_price_alerts "AAPL" "150"
echo ""

# Show an example of a buy opportunity check
buy_dips_example "AAPL" "145" 5

echo ""
echo "========================================="
echo "Remember: Always verify prices before trading!"
echo "========================================="
