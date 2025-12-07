# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import time
import os
import joblib
from typing import List, Any

# Path to model artifact (folder 'models' in repo root or backend/)
MODEL_PATH = os.path.join("models", "rec_model.pkl")

def load_recommendation_model():
    """
    Loads trained model if available. Returns a callable that accepts user_id.
    If model missing or fails to load, returns a placeholder function.
    """
    if os.path.exists(MODEL_PATH):
        try:
            print(f"Loading trained model from {MODEL_PATH}...")
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
            # Safely get version if available
            version = getattr(model, "version", "1.0")
            def predict(user_id: int) -> List[str]:
                # Example usage; replace with model.predict when using a real model
                return [f"item_{user_id}_A_v{version}", f"item_{user_id}_B_v{version}"]
            return predict
        except Exception as e:
            print(f"Error loading model: {e}. Using placeholder.")
    else:
        print(f"Model file not found at {MODEL_PATH}. Using placeholder.")

    # Placeholder predictor
    def placeholder(user_id: int) -> List[str]:
        return [f"item_{user_id}_A", f"item_{user_id}_B", f"item_{user_id}_C"]
    return placeholder

RECOMMENDATION_MODEL = load_recommendation_model()

app = FastAPI(
    title="Real-time Recommendation API",
    description="Serves personalized item recommendations.",
    version="1.0.0"
)

class UserQuery(BaseModel):
    user_id: int
    context_data: dict = {}

@app.get("/health")
def health_check():
    """Health check endpoint for ops/monitoring."""
    return {"status": "ok", "model_version": "v1.0"}

@app.post("/recommend")
def get_recommendations(query: UserQuery):
    """
    Generates real-time recommendations for a given user ID.
    """
    start_time = time.time()
    recommendations = RECOMMENDATION_MODEL(query.user_id)
    latency_ms = (time.time() - start_time) * 1000
    return {
        "user_id": query.user_id,
        "recommendations": recommendations,
        "latency_ms": round(latency_ms, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
