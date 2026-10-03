"""Evaluate once on the untouched test set and save metrics and confusion matrix."""
import os
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow import keras

LABELS = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal",
          "Shirt", "Sneaker", "Bag", "Ankle boot"]


def main():
    with np.load("data/processed/fashion_mnist.npz") as data:
        x_test, y_test = data["x_test"], data["y_test"]
    model = keras.models.load_model("models/model.h5", compile=False)
    probabilities = model.predict(x_test, verbose=0)
    predictions = probabilities.argmax(axis=1)
    loss = keras.losses.sparse_categorical_crossentropy(y_test, probabilities)
    metrics = {"test_loss": float(np.mean(loss)),
               "test_accuracy": float(np.mean(predictions == y_test)),
               "test_samples": int(len(y_test))}
    encoded = json.dumps(metrics, indent=2) + "\n"
    Path("metrics.json").write_text(encoded, encoding="utf-8")
    Path("reports").mkdir(exist_ok=True)
    # The cached copy satisfies remote versioning; root metrics stay Git-readable.
    Path("reports/metrics.json").write_text(encoded, encoding="utf-8")
    matrix = confusion_matrix(y_test, predictions, labels=np.arange(10))
    fig, ax = plt.subplots(figsize=(10, 9))
    ConfusionMatrixDisplay(matrix, display_labels=LABELS).plot(
        ax=ax, cmap="Blues", xticks_rotation=45, colorbar=False)
    ax.set_title("Fashion-MNIST test confusion matrix")
    fig.tight_layout()
    fig.savefig("reports/confusion_matrix.png", dpi=150)
    plt.close(fig)
    print(encoded)


if __name__ == "__main__":
    main()
