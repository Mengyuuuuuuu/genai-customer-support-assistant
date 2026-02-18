from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


DEFAULT_DATA_PATH = os.path.join("data", "customer_questions.csv")


@dataclass
class ClassifierResult:
    label: str
    confidence: float


class TextClassifier:
    """
    Lightweight text classifier: TF-IDF + Logistic Regression
    Provides label prediction + confidence (max class probability).
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
                ("clf", LogisticRegression(max_iter=200)),
            ]
        )
        self.pipeline.fit(X, y)

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
            raise RuntimeError("Classifier not trained yet. Call train() first.")


# Singleton-like helper for simple usage in workflow
_classifier = TextClassifier()
_is_trained = False


def ensure_trained(csv_path: str = DEFAULT_DATA_PATH) -> None:
    global _is_trained
    if not _is_trained:
        _classifier.train(csv_path=csv_path)
        _is_trained = True


def predict_category(text: str) -> str:
    ensure_trained()
    return _classifier.predict(text)


def predict_category_with_confidence(text: str) -> Tuple[str, float]:
    ensure_trained()
    r = _classifier.predict_with_confidence(text)
    return r.label, r.confidence
