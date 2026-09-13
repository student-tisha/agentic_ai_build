import agent

agent.reset_demo()
agent.data.shipments[0]["status"] = "delayed"
result = agent.resolve_disruption("SHIP-001")
print(result["resolved"], result["attempts"])