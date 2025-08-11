set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SCRIPT_DIR}/.."
IMAGE_NAME="homework8/tweet-writer:latest"

docker build -t "${IMAGE_NAME}" "${ROOT}"
echo "Built ${IMAGE_NAME}"
