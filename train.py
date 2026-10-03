"""Train the parameterized fully connected ANN (no convolutions)."""
import os
os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
import csv
from pathlib import Path
import numpy as np
import tensorflow as tf
import yaml


def main():
    with open("params.yaml", encoding="utf-8") as stream:
        params = yaml.safe_load(stream)["train"]
    tf.keras.utils.set_random_seed(params["seed"])
    tf.config.experimental.enable_op_determinism()
    with np.load("data/processed/fashion_mnist.npz") as data:
        x_train, y_train = data["x_train"], data["y_train"]
        x_val, y_val = data["x_val"], data["y_val"]
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=x_train.shape[1:]),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(params["dense_units"], activation="relu"),
        tf.keras.layers.Dropout(params["dropout_rate"]),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(params["learning_rate"]),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    history = model.fit(x_train, y_train, validation_data=(x_val, y_val),
                        epochs=params["epochs"], batch_size=params["batch_size"],
                        verbose=2)
    Path("models").mkdir(exist_ok=True)
    model.save("models/model.h5")
    with open("models/history.csv", "w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["epoch", *history.history])
        for i in range(len(history.epoch)):
            writer.writerow([i + 1, *(values[i] for values in history.history.values())])


if __name__ == "__main__":
    main()
