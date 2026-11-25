"""Transparent illustrative scenario models."""
import numpy as np

def severity(ratio):
    if ratio <= 0.05: return "Low"
    if ratio <= 0.15: return "Moderate"
    if ratio <= 0.35: return "High"
    return "Critical"

def pack(metric, unit, before, after, ratio, explanation, details):
    before, after = float(max(0, before)), float(max(0, after))
    return {"metric":metric,"unit":unit,"baseline":round(before,2),"projected":round(after,2),
            "change":round(after-before,2),"severity":severity(ratio),
            "explanation":explanation,"details":details}

def run_simulation(category, p):
    if category == "Traffic Congestion":
        demand=float(p["vehicles"]); capacity=float(p["capacity"])
        baseline=max(0,(demand-capacity)/max(capacity,1)*100)
        demand_factor=(1-p["public_transport_usage"]/100*0.22)*(1-p["carpool_reduction"]/100*0.35)
        adjusted_demand=demand*demand_factor
        adjusted_capacity=capacity*(1+p["road_expansion"]/100)
        signal_factor=max(.65,1-p["smart_signals"]/100*.25)
        projected=max(0,(adjusted_demand*signal_factor-adjusted_capacity)/max(adjusted_capacity,1)*100)
        return pack("Congestion pressure","%",baseline,projected,baseline/100,
                    "Traffic pressure is estimated by comparing effective vehicle demand with road capacity. Public transport, carpooling, signal optimisation and road expansion modify the illustrative model.",
                    {"vehicles_per_hour":demand,"road_capacity":capacity,"adjusted_demand":round(adjusted_demand,2),
                     "adjusted_capacity":round(adjusted_capacity,2),"population_density":p["population_density"]})
    if category == "Water Shortage":
        demand=float(p["demand_mld"]); supply=float(p["supply_mld"])
        baseline=max(0,demand-supply)
        extra=supply*p["leakage_reduction"]/100 + demand*p["rainwater"]/100
        adjusted_supply=supply+extra
        adjusted_demand=demand*(1-p["conservation"]/100)
        projected=max(0,adjusted_demand-adjusted_supply)
        return pack("Water deficit","MLD",baseline,projected,baseline/max(demand,1),
                    "Water deficit is estimated from daily demand and available supply. Conservation reduces demand; rainwater harvesting and leakage reduction increase usable supply.",
                    {"demand_mld":demand,"supply_mld":supply,"adjusted_demand_mld":round(adjusted_demand,2),
                     "adjusted_supply_mld":round(adjusted_supply,2),"reservoir_availability_pct":p["reservoir_availability"],
                     "population":p["population"],"consumption_lpcd":p["consumption_lpcd"]})
    generated=float(p["waste_tpd"]); capacity=float(p["collection_capacity"])
    baseline=max(0,generated-capacity)
    diversion=generated*(p["recycling"]+p["segregation"]*.35+p["composting"]*.5)/100
    effective_capacity=capacity*(1+p["collection_efficiency"]/100)
    projected=max(0,generated-diversion-effective_capacity)
    return pack("Uncollected waste","tonnes/day",baseline,projected,baseline/max(generated,1),
                "Uncollected waste is estimated after collection capacity and assumed recycling, segregation and composting diversion are applied.",
                {"waste_generated_tpd":generated,"collection_capacity_tpd":capacity,
                 "estimated_diversion_tpd":round(diversion,2),"effective_collection_capacity_tpd":round(effective_capacity,2),
                 "population":p["population"]})
