"""
Procurement Process Optimization

This script optimizes replenishment frequency to minimize total costs
including transportation, capital, and storage costs.
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize_scalar
import math


def calculate_total_cost(Q, D_annual, cost_per_unit, transport_cost,
                         capital_rate, storage_cost):
    """
    Calculate total annual cost for a given order quantity Q.

    Parameters:
    - Q: Order quantity (units)
    - D_annual: Annual demand (units)
    - cost_per_unit: Unit cost ($)
    - transport_cost: Cost per order ($)
    - capital_rate: Annual capital cost rate (%)
    - storage_cost: Storage cost per unit per year ($)
    """
    if Q <= 0:
        return float('inf')

    # Number of orders per year
    n_orders = D_annual / Q

    # Transportation cost
    total_transport = n_orders * transport_cost

    # Average inventory
    avg_inventory = Q / 2

    # Capital cost (financing inventory)
    capital_cost = avg_inventory * cost_per_unit * capital_rate

    # Storage cost
    total_storage = avg_inventory * storage_cost

    # Total cost
    total = total_transport + capital_cost + total_storage

    return total


def optimize_order_quantity(D_annual, cost_per_unit, transport_cost,
                           capital_rate, storage_cost):
    """
    Find the optimal order quantity that minimizes total cost.

    Uses scipy optimization to find minimum.
    """
    # Define objective function
    def objective(Q):
        return calculate_total_cost(
            Q, D_annual, cost_per_unit, transport_cost,
            capital_rate, storage_cost
        )

    # Optimize
    result = minimize_scalar(
        objective,
        bounds=(1, D_annual),
        method='bounded'
    )

    return result.x, result.fun


def economic_order_quantity(D_annual, transport_cost, holding_cost_rate):
    """
    Calculate EOQ using classic formula.

    EOQ = sqrt(2 * D * S / H)
    where:
    - D: Annual demand
    - S: Setup/ordering cost
    - H: Holding cost per unit per year
    """
    eoq = math.sqrt((2 * D_annual * transport_cost) / holding_cost_rate)
    return eoq


def analyze_sku(sku_name, D_annual, cost_per_unit, transport_cost,
                capital_rate=0.10, storage_cost_per_unit=2.0):
    """Analyze optimal procurement for a single SKU."""
    print(f"\n--- SKU: {sku_name} ---")
    print(f"Annual demand: {D_annual:,} units")
    print(f"Unit cost: ${cost_per_unit:.2f}")
    print(f"Transport cost per order: ${transport_cost:.2f}")
    print(f"Capital rate: {capital_rate*100:.1f}%")
    print(f"Storage cost: ${storage_cost_per_unit:.2f}/unit/year")

    # Holding cost = capital cost + storage cost
    holding_cost = cost_per_unit * capital_rate + storage_cost_per_unit

    # Classic EOQ
    eoq = economic_order_quantity(D_annual, transport_cost, holding_cost)
    print(f"\nEOQ (classic formula): {eoq:.0f} units")

    # Optimized Q
    opt_Q, opt_cost = optimize_order_quantity(
        D_annual, cost_per_unit, transport_cost,
        capital_rate, storage_cost_per_unit
    )
    print(f"Optimized Q: {opt_Q:.0f} units")
    print(f"Minimum total cost: ${opt_cost:,.2f}/year")

    # Cost breakdown at optimal Q
    n_orders = D_annual / opt_Q
    avg_inventory = opt_Q / 2

    print(f"\nAt optimal Q:")
    print(f"  Orders per year: {n_orders:.1f}")
    print(f"  Average inventory: {avg_inventory:.0f} units")
    print(f"  Days of supply: {(opt_Q / D_annual) * 365:.1f} days")

    return opt_Q, opt_cost


def compare_order_quantities(D_annual, cost_per_unit, transport_cost,
                            capital_rate, storage_cost):
    """Compare costs for different order quantities."""
    print("\n" + "-" * 60)
    print("ORDER QUANTITY COMPARISON")
    print("-" * 60)

    quantities = [50, 100, 200, 500, 1000, 2000]
    print(f"{'Q':<10} {'Orders/Yr':<12} {'Total Cost':<15} {'Days Supply':<12}")
    print("-" * 50)

    for Q in quantities:
        cost = calculate_total_cost(
            Q, D_annual, cost_per_unit, transport_cost,
            capital_rate, storage_cost
        )
        n_orders = D_annual / Q
        days_supply = (Q / D_annual) * 365
        print(f"{Q:<10} {n_orders:<12.1f} ${cost:<14,.2f} {days_supply:<12.1f}")


def main():
    """Main function for procurement optimization."""
    print("=" * 60)
    print("PROCUREMENT PROCESS OPTIMIZATION")
    print("=" * 60)

    # Sample SKUs
    skus = [
        {"name": "SKU-A", "demand": 12000, "unit_cost": 25.00, "transport": 150},
        {"name": "SKU-B", "demand": 5000, "unit_cost": 100.00, "transport": 200},
        {"name": "SKU-C", "demand": 50000, "unit_cost": 5.00, "transport": 100},
    ]

    capital_rate = 0.10  # 10% annual
    storage_cost = 2.0   # $2 per unit per year

    for sku in skus:
        analyze_sku(
            sku["name"],
            sku["demand"],
            sku["unit_cost"],
            sku["transport"],
            capital_rate,
            storage_cost
        )

    # Detailed comparison for first SKU
    print("\n" + "=" * 60)
    compare_order_quantities(
        skus[0]["demand"],
        skus[0]["unit_cost"],
        skus[0]["transport"],
        capital_rate,
        storage_cost
    )


if __name__ == "__main__":
    main()
