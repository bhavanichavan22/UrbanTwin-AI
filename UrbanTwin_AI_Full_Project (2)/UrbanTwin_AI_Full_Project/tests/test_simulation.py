from urbantwin.simulation import run_simulation

def test_traffic_outputs_nonnegative():
    p={"vehicles":8500,"capacity":6000,"population_density":12000,"public_transport_usage":30,
       "smart_signals":20,"road_expansion":5,"carpool_reduction":10}
    r=run_simulation("Traffic Congestion",p)
    assert r["baseline"]>=0 and r["projected"]>=0

def test_water_shortage_projection_nonnegative():
    p={"demand_mld":180,"supply_mld":145,"reservoir_availability":60,"population":850000,
       "consumption_lpcd":135,"conservation":10,"rainwater":15,"leakage_reduction":10}
    r=run_simulation("Water Shortage",p)
    assert r["projected"]>=0

def test_waste_outputs_nonnegative():
    p={"waste_tpd":350,"collection_capacity":270,"population":850000,"recycling":20,
       "segregation":25,"collection_efficiency":15,"composting":15}
    r=run_simulation("Waste Accumulation",p)
    assert r["projected"]>=0

def test_intervention_reduces_traffic_pressure():
    base={"vehicles":8500,"capacity":6000,"population_density":12000,"public_transport_usage":0,
          "smart_signals":0,"road_expansion":0,"carpool_reduction":0}
    better={**base,"public_transport_usage":40,"smart_signals":30,"carpool_reduction":20}
    assert run_simulation("Traffic Congestion",better)["projected"] <= run_simulation("Traffic Congestion",base)["projected"]
