from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DEFAULT_DATA_PATH = os.path.join("data", "customer_questions.csv")
DEFAULT_MODEL_PATH = os.path.join("models", "text_classifier.joblib")


@dataclass
class ClassifierResult:
    label: str
    confidence: float


class TextClassifier:
    """
    TF-IDF + Logistic Regression classifier.
    Supports training, saving/loading, and confidence (max class probability).
    """

    def __init__(self) -> None:
        self.pipeline: Pipeline | None = None

    def train(self, csv_path: str = DEFAULT_DATA_PATH) -> None:
        df = pd.read_csv(csv_path)
        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("CSV must contain columns: text,label")

        X = df["text"].astype(str).tolist()
        y = df["label"].astype(str).tolist()

        self.pipeline = Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                ("clf", LogisticRegression(max_iter=300)),
            ]
        )
        self.pipeline.fit(X, y)

    def save(self, model_path: str = DEFAULT_MODEL_PATH) -> None:
        if self.pipeline is None:
            raise RuntimeError("Nothing to save. Train or load a model first.")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.pipeline, model_path)

    def load(self, model_path: str = DEFAULT_MODEL_PATH) -> bool:
        if not os.path.exists(model_path):
            return False
        self.pipeline = joblib.load(model_path)
        return True

    def predict(self, text: str) -> str:
        self._ensure_ready()
        return str(self.pipeline.predict([text])[0])  # type: ignore[union-attr]

    def predict_with_confidence(self, text: str) -> ClassifierResult:
        self._ensure_ready()
        proba = self.pipeline.predict_proba([text])[0]  # type: ignore[union-attr]
        classes = self.pipeline.classes_  # type: ignore[union-attr]
        idx = int(proba.argmax())
        return ClassifierResult(label=str(classes[idx]), confidence=float(proba[idx]))

    def _ensure_ready(self) -> None:
        if self.pipeline is None:
            raise RuntimeError("Model not ready. Train or load first.")


_classifier = TextClassifier()


def ensure_model_ready(
    csv_path: str = DEFAULT_DATA_PATH,
    model_path: str = DEFAULT_MODEL_PATH,
) -> None:
    """
    Try load model first; if not available, train and save it.
    """
    loaded = _classifier.load(model_path=model_path)
    if not loaded:
        _classifier.train(csv_path=csv_path)
        _classifier.save(model_path=model_path)


def predict_category(text: str) -> str:
    ensure_model_ready()
    return _classifier.predict(text)


def predict_category_with_confidence(text: str) -> Tuple[str, float]:
    ensure_model_ready()
    r = _classifier.predict_with_confidence(text)
    return r.label, r.confidence


if __name__ == "__main__":
    # manual training entrypoint:
    # python src/classifier.py
    ensure_model_ready()
    print(f"✅ Model ready (saved to: {DEFAULT_MODEL_PATH})")
