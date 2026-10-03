# Running the assignment

Run all commands from the repository root with Python 3.12 in an activated
virtual environment. The repository intentionally keeps data/model payloads in
DVC rather than Git.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
dvc pull
dvc repro
python verify_pipeline.py
```

If remote access is unavailable, `dvc repro` can regenerate the pipeline from
the public Fashion-MNIST source. The first prepare stage requires Internet.
For exact dependency versions from the executed environment, use
`requirements-lock.txt` when present.

## Google Drive

The default remote is the updated assignment folder:
https://drive.google.com/drive/folders/1WCgR7ugUC_VjKzU-36cxLQN-WfbN2n-q

```powershell
dvc remote list
dvc push
```

The main branch points to the replacement folder and its data cache has been
verified in sync. Use `dvc push` for the current branch. Some historical commits
from the simulated exercises still contain the old folder URL, so a blanket
`dvc push --all-branches --all-tags` may contact that previous account. The v1,
teammate-sim, and centered-normalization objects were separately pushed to the
replacement folder using its URL and verified there.

Each person authenticates with their own Google account. Never commit cached
OAuth tokens, a service account key, or `.dvc/config.local`. If the default DVC
OAuth application is blocked by Google, follow the official custom desktop
OAuth client instructions at
https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive
and configure credentials using `dvc remote modify --local`.

With a downloaded Desktop client JSON, the included helper handles local-only
configuration without printing its secrets:

```powershell
python connect_drive.py "C:\path\to\client_secret.json"
```

In Google Cloud, enable the Google Drive API. Create/configure the OAuth consent
screen and add your Google account as a test user if the app is in Testing mode.
Create an OAuth client of type Desktop app and download its JSON. Authenticate
with the account that owns the assignment Drive folder. The completed upload was
verified with `dvc status --cloud` and a read-only inventory of the Drive folder.
For the rubric's browser screenshot, open the folder and capture its contents.
Share the folder with the instructor's Google account.

## History and evidence

- `dev`: incremental feature implementation and pipeline experiments.
- `hotfix`: README spelling fix merged into main before rebasing dev.
- `evidence-reset-soft` and `evidence-reset-hard`: preserve the throwaway commits
  so the reset demonstration remains inspectable after their scratch branch resets.
- `teammate-sim`: float64 normalization and its independently generated pointer.
- `v1`: standalone DVC baseline, merged into main before the conflict exercise.
- `conflict-resolved`: reconciled preprocessing code and authoritative data pointer.
- `pipeline-v1`: four-stage pipeline with 128 hidden units.
- `v2`: the same pipeline with 256 hidden units.

The assignment asks for both standalone `.dvc` pointers and pipeline outputs
for identical paths. DVC cannot have two stages own the same output. The history
therefore demonstrates standalone tracking and pointer conflicts first, then
uses `dvc remove` (metadata only) to migrate to `dvc.yaml` and `dvc.lock`.
Root `metrics.json` is a non-cached DVC metric committed to Git; its identical
copy in the DVC-cached `reports/` directory also travels to Drive.

The conflict variants are demonstrations, not additional model experiments.
The final normalization clips to the pixel domain, divides in float64, then
casts to float32. For uint8 Fashion-MNIST it matches the original [0, 1] mapping.
The test set is untouched during splitting and training. Only validation data
is passed to `model.fit`.

Fixed seeds and deterministic TensorFlow operations support repeatability.
Numerical identity across different hardware and dependency versions is not
guaranteed. DVC hashes record the actual artifacts from each run.

## Individual scripts

```powershell
python src/prepare.py
python src/preprocess.py
python src/train.py
python src/evaluate.py
```

These commands are for standalone demonstration. Use `dvc repro` for normal
work so lock-file hashes and dependency tracking are refreshed consistently.
