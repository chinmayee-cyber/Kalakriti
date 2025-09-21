from agents.trend_agent import run_trend_agent_one_shot
from agents.prediction_agent import price_prediction_agent

if __name__ == "__main__":
    # Run trend analysis
    print("Running trend analysis...")
    result = run_trend_agent_one_shot()
    print(f"Trend analysis completed: {result}")
    
    # Example price prediction
    metadata = {"medium": "Oil", "size_bucket": "size_2"}
    embedding = [0.01, 0.02, 0.03, 0.04]  # dummy vector
    
    response = price_prediction_agent(
        input={"metadata": metadata, "embedding": embedding}
    )
    
    print("Price prediction:")
    print(response)