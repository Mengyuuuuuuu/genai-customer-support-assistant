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
Text Classification (Logistic Regression + TF-IDF)  
↓  
LLM Response Generation  
↓  
Evaluation / Guardrails  

## Dataset
Synthetic dataset generated for prototyping purposes.

## Hypothesis
A GenAI workflow can reduce manual handling effort in customer support by automatically classifying and responding to typical customer inquiries.

## Future Improvements
- RAG integration
- Feedback loop
- Confidence-based fallback logic
- Deployment as API / Streamlit app
