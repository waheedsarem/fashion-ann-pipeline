# Fashion-MNIST ANN Pipeline

Assignment 3: reproducible Fashion-MNIST classification with TensorFlow, Git and DVC.

The project trains a fully connected ANN on Fashion-MNIST and versions raw data,
processed data, models and evaluation outputs. Run the entire pipeline with
`dvc repro` from the repository root in an activated Python environment.

| Version | Hidden units | Test accuracy | Test loss |
| --- | ---: | ---: | ---: |
| v1 | 128 | 88.37% | 0.337296 |
| v2 | 256 | 88.43% | 0.340086 |

Both runs exceed the assignment's 85% target on the official 10,000-image test
set. The small accuracy increase is 0.06 percentage points; test loss increased,
so v2 is not uniformly better. All other hyperparameters stay fixed.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
dvc repro
python verify_pipeline.py
```

See [setup and history notes](README_SETUP.md) for standalone commands, remote
configuration and the rationale for migrating `.dvc` pointers to pipeline outputs.
The four-page report is in [submission/Assignment3_Report.pdf](submission/Assignment3_Report.pdf).
Full captured command outputs are under [evidence/](evidence/).

## Google Drive status

The default DVC remote points to the updated
[assignment folder](https://drive.google.com/drive/folders/1WCgR7ugUC_VjKzU-36cxLQN-WfbN2n-q).
Google OAuth was completed after adding the account as a tester for project
`sonorous-haven-510508-a0`. The v1, v2, and both simulated preprocessing variants
were pushed to the replacement folder. DVC reports the current cache and remote
in sync. A Drive API inventory confirmed 21 folders and 20 files, including 12
hash-named DVC objects (178,413,292 reported bytes).

## Pipeline

`prepare -> preprocess -> train -> evaluate`

The preprocessing split is stratified: 48,000 training, 12,000 validation and
10,000 test examples. Architecture: Flatten, Dense(ReLU), Dropout, Dense(10,
Softmax). Training uses Adam and sparse categorical cross-entropy for 20 epochs.
Changing only `train.dense_units` reruns train and evaluate, while DVC skips the
unchanged prepare and preprocess stages.

Code and Git-readable metrics are committed to Git. Data, HDF5 models, training
history and the reports directory are cached by DVC; no credentials are tracked.
