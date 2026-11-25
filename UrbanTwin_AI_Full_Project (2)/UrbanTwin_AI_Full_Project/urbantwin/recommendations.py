"""Rule-based recommendation engine with reasons and priority."""
def recommend(category, result, params):
    severity=result["severity"]
    if category=="Traffic Congestion":
        items=[
        ("Improve public transport frequency","Reduces private vehicle dependence and can lower peak-hour road demand.",1),
        ("Optimise traffic signals at bottleneck junctions","Coordinated signals can reduce avoidable queueing and stop-start delay.",2),
        ("Promote carpooling and staggered timings","Shifts or reduces peak-period vehicle demand without immediately expanding roads.",3),
        ("Evaluate targeted road-capacity changes","Consider only after corridor-level counts and environmental and land-use review.",4)]
    elif category=="Water Shortage":
        items=[
        ("Repair high-loss distribution zones","Leakage reduction can recover supply that is already treated and pumped.",1),
        ("Introduce demand management and conservation","Reduces pressure on limited supply while protecting essential household needs.",2),
        ("Expand rainwater harvesting and reuse","Adds supplementary water sources when storage, quality and seasonal conditions permit.",3),
        ("Monitor reservoirs and ward-level demand","Improves early warning and helps allocate supply transparently.",4)]
    else:
        items=[
        ("Strengthen source segregation","Improves the quality of recyclable and compostable material streams.",1),
        ("Optimise collection routes and schedules","Can reduce missed pickups and make better use of collection capacity.",2),
        ("Expand composting and recycling capacity","Diverts suitable waste away from disposal sites.",3),
        ("Track ward-level generation and collection","Makes service gaps visible and supports evidence-based resource allocation.",4)]
    if severity=="Critical":
        items=items[:]
    return [{"title":x[0],"reason":x[1],"priority":x[2]} for x in items]
