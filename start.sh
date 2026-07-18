#!/bin/sh

# Exit on any error
set -e

# --- Script Configuration ---
CONTAINER_NAME="isro-checker"
IMAGE_NAME="shankershawn/isro-mission-checker"
ARCH_SUFFIX="linux-armv7l"

# --- Determine Image Version ---
if [ -n "$1" ]; then
  # Use the version provided as a command-line argument.
  VERSION=$1
  echo "Using specified version: $VERSION"
else
  # No version specified, find the latest tag.
  LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
  echo "No version specified, using latest tag: $LATEST_TAG"

  # Use the same robust parsing as build.sh to handle pre-release tags.
  VERSION_CORE=$(echo "$LATEST_TAG" | sed -e 's/^v//' -e 's/-.*//')
  PADDED_VERSION="${VERSION_CORE}.0.0"
  MAJOR=$(echo "$PADDED_VERSION" | cut -d. -f1)
  MINOR=$(echo "$PADDED_VERSION" | cut -d. -f2)
  PATCH=$(echo "$PADDED_VERSION" | cut -d. -f3)
  VERSION="v${MAJOR}.${MINOR}.${PATCH}"
fi
# ---

IMAGE_TAG="${VERSION}-${ARCH_SUFFIX}"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

echo "Preparing to start container '$CONTAINER_NAME' with image '$FULL_IMAGE_NAME'..."

# --- Securely Read Password ---
printf "Enter GMAIL_PASSWORD: "
stty -echo
read GMAIL_PASSWORD
stty echo
echo ""

if [ -z "$GMAIL_PASSWORD" ]; then
  echo "Error: GMAIL_PASSWORD cannot be empty." >&2
  exit 1
fi

# --- Manage Existing Container ---
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Found an existing container named '$CONTAINER_NAME'. Removing it..."
  docker stop "$CONTAINER_NAME" >/dev/null
  docker rm "$CONTAINER_NAME" >/dev/null
  echo "Removed existing container."
fi

# --- Start New Container ---
echo "Starting new container..."
docker run \
  --restart=always \
  -tid \
  --name "$CONTAINER_NAME" \
  -e "GMAIL_PASSWORD=${GMAIL_PASSWORD}" \
  "$FULL_IMAGE_NAME"

echo ""
echo "Successfully launched container '$CONTAINER_NAME'."
echo "To view its logs, run: docker logs $CONTAINER_NAME"
echo "To stop it, run: docker stop $CONTAINER_NAME"
