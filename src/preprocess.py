"""Normalize images and make a stratified validation split."""
from pathlib import Path
import numpy as np
import yaml
from sklearn.model_selection import train_test_split


def normalize(images):
    return (np.clip(images, 0, 255).astype(np.float64) / 255.0).astype(np.float32)


def main():
    with open("params.yaml", encoding="utf-8") as stream:
        params = yaml.safe_load(stream)["preprocess"]
    with np.load("data/raw/fashion_mnist.npz") as raw:
        x_train, x_val, y_train, y_val = train_test_split(
            normalize(raw["x_train"]), raw["y_train"],
            test_size=params["test_size"], random_state=params["seed"],
            stratify=raw["y_train"])
        output = Path("data/processed")
        output.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(output / "fashion_mnist.npz", x_train=x_train,
                            y_train=y_train, x_val=x_val, y_val=y_val,
                            x_test=normalize(raw["x_test"]), y_test=raw["y_test"])
    print(f"Prepared train={len(y_train)}, validation={len(y_val)}, test=10000.")


if __name__ == "__main__":
    main()

# Validation splitting is stratified to preserve class balance.
