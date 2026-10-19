# ⚡ DeFi Liquidation Bot

Production-grade DeFi liquidation bot with flash loan integration.

## Strategy
1. Monitor unhealthy positions (Health Factor < 1.0)
2. Calculate optimal liquidation amount
3. Execute flash loan to acquire collateral token
4. Liquidate position, receive discounted collateral (5-8% bonus)
5. Swap collateral to repay flash loan
6. Pocket the profit

## Supported Protocols
- Aave V2/V3, Compound III, MakerDAO, Euler Finance

## Performance
- Scans 1000+ positions per second
- Sub-block execution via Flashbots bundles
- Auto-adjusting gas price strategies
