"""Check data invariants, model structure and reported test accuracy after repro."""
import csv
import json
from pathlib import Path
import numpy as np
import yaml
from tensorflow import keras

params = yaml.safe_load(Path('params.yaml').read_text())
with np.load('data/raw/fashion_mnist.npz') as raw:
    assert raw['x_train'].shape == (60000, 28, 28)
    assert raw['x_test'].shape == (10000, 28, 28)
with np.load('data/processed/fashion_mnist.npz') as data:
    for name in ['x_train','x_val','x_test']:
        assert data[name].dtype == np.float32
        assert np.isfinite(data[name]).all()
        assert 0 <= data[name].min() <= data[name].max() <= 1
    assert len(data['x_train']) + len(data['x_val']) == 60000
    assert len(data['x_val']) == round(60000 * params['preprocess']['test_size'])
    assert np.array_equal(data['y_test'], np.load('data/raw/fashion_mnist.npz')['y_test'])
model = keras.models.load_model('models/model.h5', compile=False)
assert [type(layer).__name__ for layer in model.layers] == ['Flatten','Dense','Dropout','Dense']
assert model.layers[1].units == params['train']['dense_units']
assert model.layers[-1].units == 10
with open('models/history.csv', newline='') as stream:
    assert len(list(csv.DictReader(stream))) == params['train']['epochs']
metrics = json.loads(Path('metrics.json').read_text())
assert metrics == json.loads(Path('reports/metrics.json').read_text())
assert metrics['test_samples'] == 10000
assert metrics['test_accuracy'] >= 0.85, metrics
assert Path('reports/confusion_matrix.png').stat().st_size > 1000
print('PASS: data shapes/range, labels, ANN topology, history, metrics and >=85% accuracy')
print(json.dumps(metrics, indent=2))
