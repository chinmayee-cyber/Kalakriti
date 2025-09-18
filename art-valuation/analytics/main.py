from google.adk import registry
from agents.metadata_agent import MetadataAgent
from agents.valuation_agent import ValuationAgent

def register_agents():
    registry.register_agent_class("metadata", MetadataAgent)
    registry.register_agent_class("valuation", ValuationAgent)
