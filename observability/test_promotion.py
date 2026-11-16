"""Exercise the actual manual promotion job with local GitHub fixtures."""
import json
import os
from pathlib import Path
import subprocess

import pytest
import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/deploy.yml"
REPO = "Usmanovkairat/splitwise-pro"
REVISION = "a" * 40
DIGEST = "sha256:" + "e" * 64
IMAGE = f"ghcr.io/{REPO.lower()}@{DIGEST}"
TRUSTED_RUN = {
    "conclusion": "success",
    "event": "push",
    "head_branch": "main",
    "head_repository": {"full_name": REPO},
    "path": ".github/workflows/ci.yml",
    "run_attempt": 2,
    "head_sha": REVISION,
}


@pytest.mark.parametrize(
    ("run_updates", "artifact_updates", "run_id", "expected"),
    [
        ({}, {}, "123", True),
        ({"event": "pull_request"}, {}, "123", False),
        ({"conclusion": "failure"}, {}, "123", False),
        ({"path": ".github/workflows/other.yml"}, {}, "123", False),
        ({"head_repository": {"full_name": "other/fork"}}, {}, "123", False),
        ({}, {"revision": "b" * 40}, "123", False),
        ({}, {"image": f"ghcr.io/{REPO.lower()}:latest"}, "123", False),
        ({}, {"image": f"example.com/else@{DIGEST}"}, "123", False),
        ({}, {}, "invalid", False),
    ],
)
def test_promotion_gate(tmp_path, run_updates, artifact_updates, run_id, expected):
    workflow = yaml.safe_load(WORKFLOW.read_text())
    assert set(workflow[True]) == {"workflow_dispatch"}
    jobs = workflow["jobs"]
    assert jobs["deploy"]["needs"] == "verify-release"
    assert jobs["deploy"]["environment"] == "production"
    command = jobs["verify-release"]["steps"][0]["run"]
    stub = tmp_path / "gh"
    stub.write_text("""#!/bin/bash
set -eu
if [ "$1" = api ]; then
  test "$2" = "repos/$REPO/actions/runs/$RUN_ID"
  cat workflow.json
else
  test "$7" = verified-development-2
  mkdir -p release
  cp fixture.json release/release.json
fi
""")
    stub.chmod(0o755)
    (tmp_path / "workflow.json").write_text(json.dumps(TRUSTED_RUN | run_updates))
    (tmp_path / "fixture.json").write_text(json.dumps(
        {"revision": REVISION, "image": IMAGE} | artifact_updates
    ))
    output = tmp_path / "result"
    env = os.environ | {
        "PATH": f"{tmp_path}:{os.environ['PATH']}",
        "REPO": REPO,
        "RUN_ID": run_id,
        "GITHUB_OUTPUT": str(output),
    }
    result = subprocess.run(["bash", "-c", command], cwd=tmp_path, env=env,
                            capture_output=True, text=True, check=False)
    assert (result.returncode == 0) is expected, result.stderr
    if expected:
        assert output.read_text().splitlines() == [f"image={IMAGE}", f"revision={REVISION}"]
    else:
        assert not output.exists()
