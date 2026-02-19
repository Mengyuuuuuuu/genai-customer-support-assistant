# GenAI Customer Support Assistant

## Overview

This project demonstrates an end-to-end GenAI-powered customer support workflow for the energy sector.

The system combines:

- Classical ML-based text classification (category + confidence score)
- Confidence-based workflow routing (3-tier decision logic)
- Controlled LLM response generation (Qwen via OpenAI-compatible API)
- Deterministic dialog strategy (LLM follow-up behavior controlled by workflow)

The architecture separates classification, orchestration, and generation layers to ensure predictable and explainable system behavior.


## Architecture

User Input
   ↓
Classifier (category + confidence)
   ↓
Workflow Router (3-tier decision logic)
   ↓
LLM (Qwen)
   ↓
Final Response


## Dataset
A synthetic dataset was programmatically generated using Python to simulate typical customer service inquiries across predefined categories. 
The dataset is used for classifier training and prototyping purposes and does not contain real user data.


## Hypothesis

A structured GenAI workflow that combines classical ML classification with controlled LLM response generation can reduce manual handling effort in customer support while maintaining predictable and explainable behavior.


## Future Improvements

- RAG integration for knowledge-grounded responses
- Human-in-the-loop feedback loop for continuous classifier improvement
- Real-world dataset integration and evaluation
- API deployment (FastAPI) or Streamlit frontend
- Monitoring and logging for production readiness


## Impact of Training Data Size on Model Confidence

We evaluated the effect of increasing synthetic training data size.

- 120 samples → confidence ≈ 0.36  
- 300 samples → confidence ≈ 0.46
- 600 samples → confidence ≈ 0.57  

This demonstrates that larger training datasets improve model certainty,
even in a lightweight TF-IDF + Logistic Regression setup.


## LLM Integration

The system uses Qwen (Alibaba DashScope) via an OpenAI-compatible API endpoint.

- Model: `qwen-plus`
- Endpoint: DashScope OpenAI-compatible API
- Temperature: 0.3 (low variance for stable customer responses)

The LLM is used for:
- Generating structured customer service responses
- Producing controlled follow-up questions (medium confidence tier)
  

## Setup

Create a `.env` file:

QWEN_API_KEY=your_api_key_here
