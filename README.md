# GenAI Customer Support Assistant

## Overview
This project demonstrates an end-to-end GenAI workflow for customer support automation in the energy sector.

The system combines:
- Classical ML-based text classification
- LLM-based response generation
- Basic evaluation logic

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
Synthetic dataset generated for prototyping purposes.

## Hypothesis
A GenAI workflow can reduce manual handling effort in customer support by automatically classifying and responding to typical customer inquiries.

## Future Improvements
- RAG integration
- Feedback loop
- Confidence-based fallback logic
- Deployment as API / Streamlit app

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
