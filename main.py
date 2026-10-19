import random
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Position:
    owner: str
    collateral_token: str
    collateral_amount_usd: float
    debt_token: str
    debt_amount_usd: float
    liquidation_threshold: float = 0.825

    @property
    def health_factor(self) -> float:
        if self.debt_amount_usd == 0:
            return float("inf")
        return (self.collateral_amount_usd * self.liquidation_threshold) / self.debt_amount_usd

    @property
    def is_liquidatable(self) -> bool:
        return self.health_factor < 1.0

@dataclass
class LiquidationOpportunity:
    position: Position
    max_liquidatable_usd: float
    collateral_bonus: float = 0.05
    estimated_profit_usd: float = 0.0

    def calculate_profit(self, gas_cost_usd: float = 30.0) -> float:
        gross = self.max_liquidatable_usd * self.collateral_bonus
        self.estimated_profit_usd = gross - gas_cost_usd
        return self.estimated_profit_usd

class LiquidationBot:
    def __init__(self, min_profit_usd: float = 50.0):
        self.min_profit = min_profit_usd
        self.total_profit = 0.0
        self.executions = 0

    def scan_positions(self, positions: List[Position]) -> List[LiquidationOpportunity]:
        opportunities = []
        for pos in positions:
            if pos.is_liquidatable:
                max_liq = min(pos.debt_amount_usd * 0.5, pos.collateral_amount_usd)
                opp = LiquidationOpportunity(pos, max_liq)
                profit = opp.calculate_profit()
                if profit > self.min_profit:
                    opportunities.append(opp)
        opportunities.sort(key=lambda o: o.estimated_profit_usd, reverse=True)
        return opportunities

    def execute_liquidation(self, opp: LiquidationOpportunity) -> bool:
        print(f"  [LIQ] Liquidating {opp.position.owner[:10]}... "
              f"Debt: ${opp.max_liquidatable_usd:,.0f} | "
              f"Profit: ${opp.estimated_profit_usd:.2f}")
        self.total_profit += opp.estimated_profit_usd
        self.executions += 1
        return True

if __name__ == "__main__":
    random.seed(42)
    positions = []
    for i in range(1000):
        coll = random.uniform(1_000, 500_000)
        debt = coll * random.uniform(0.5, 1.2)
        positions.append(Position(
            owner=f"0x{i:040x}", collateral_token="ETH",
            collateral_amount_usd=coll, debt_token="USDC", debt_amount_usd=debt
        ))

    bot = LiquidationBot(min_profit_usd=20.0)
    opps = bot.scan_positions(positions)
    print(f"Found {len(opps)} liquidation opportunities from {len(positions)} positions")
    for opp in opps[:5]:
        bot.execute_liquidation(opp)
    print(f"Total executions: {bot.executions}")
    print(f"Total profit    : ${bot.total_profit:,.2f}")
