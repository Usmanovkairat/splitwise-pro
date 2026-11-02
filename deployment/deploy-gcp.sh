#!/bin/bash
# Runs on the existing protected VM, as root, after CI publishes a tested image.
set -euo pipefail
image=${1:?Usage: deploy-gcp.sh public-registry/image@sha256:digest}
if [[ ! "$image" =~ ^[a-zA-Z0-9][a-zA-Z0-9./:_-]*@sha256:[a-f0-9]{64}$ ]]; then
  echo 'An immutable image digest is required' >&2
  exit 2
fi
cd /srv/splitwise/config
exec 9>/var/lock/splitwise-deploy.lock
flock -n 9 || { echo 'Another deployment is running' >&2; exit 1; }
# Pull before disturbing the running application; VM needs anonymous image access.
docker pull "$image"
umask 077
stamp=$(date -u +%Y%m%dT%H%M%SZ)
backup="/srv/splitwise/config/compose.before-$stamp.yaml"
dump="/srv/splitwise/pre-release-$stamp.dump"
cp compose.yaml "$backup"
rollback_on_error() {
  result=$?
  if [ "$result" -ne 0 ]; then
    cp "$backup" compose.yaml
    docker compose up -d --wait --wait-timeout 180 || true
    echo "Release failed; attempted previous-image rollback. Backup: $dump. Review schema compatibility before restoring data." >&2
  fi
}
trap rollback_on_error EXIT
docker compose stop app
if ! docker compose exec -T db pg_dump -U splitwise -d splitwise --format=custom > "$dump"; then
  echo 'Backup failed; application was not upgraded' >&2
  exit 1
fi
# The template contains exactly one app image followed by the postgres image.
python3 - "$image" <<'PY'
import pathlib, re, sys
path = pathlib.Path('compose.yaml')
text = path.read_text()
text, count = re.subn(r'(  app:\n    image: )[^\n]+', lambda m: m[1] + sys.argv[1], text, count=1)
if count != 1:
    raise SystemExit('Unexpected Compose layout; refusing to change it')
path.write_text(text)
PY
if docker compose up -d --wait --wait-timeout 180 && curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/api/health; then
  trap - EXIT
  echo "Deployment healthy; previous Compose: $backup; protected backup: $dump"
else
  echo "Deployment failed; restoring the previous Compose image." >&2
  exit 1
fi
