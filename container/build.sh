#!/bin/bash
# Build the NanoClaw agent container image

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE_NAME="nanoclaw-agent"
TAG="${1:-latest}"
CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-docker}"

# Copy local MCP packages into the build context so Dockerfile can COPY them.
# Source paths are on the host; the copies are cleaned up after the build.
GOOGLE_ADS_MCP_SRC="${GOOGLE_ADS_MCP_PATH:-/home/nanoclaw_svc/mcps/google-ads-mcp}"
GOOGLE_ADS_MCP_DEST="${SCRIPT_DIR}/google-ads-mcp"

if [ -d "$GOOGLE_ADS_MCP_SRC" ]; then
  echo "Copying google-ads-mcp from $GOOGLE_ADS_MCP_SRC..."
  cp -r "$GOOGLE_ADS_MCP_SRC" "$GOOGLE_ADS_MCP_DEST"
else
  echo "WARNING: google-ads-mcp not found at $GOOGLE_ADS_MCP_SRC — skipping"
fi

echo "Building NanoClaw agent container image..."
echo "Image: ${IMAGE_NAME}:${TAG}"

${CONTAINER_RUNTIME} build -t "${IMAGE_NAME}:${TAG}" .
BUILD_EXIT=$?

# Clean up temporary build context copies
[ -d "$GOOGLE_ADS_MCP_DEST" ] && rm -rf "$GOOGLE_ADS_MCP_DEST"

exit $BUILD_EXIT

echo ""
echo "Build complete!"
echo "Image: ${IMAGE_NAME}:${TAG}"
echo ""
echo "Test with:"
echo "  echo '{\"prompt\":\"What is 2+2?\",\"groupFolder\":\"test\",\"chatJid\":\"test@g.us\",\"isMain\":false}' | ${CONTAINER_RUNTIME} run -i ${IMAGE_NAME}:${TAG}"
