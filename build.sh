#!/bin/sh

# Exit on any error
set -e

# --- Versioning Logic ---

# Get the latest git tag, or default to v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current latest tag is: $LATEST_TAG"

# --- Robust Version Parsing ---
# 1. Remove 'v' prefix.
# 2. Strip any pre-release suffix (like -alpha, -rc1) to get the core version.
# 3. Pad with ".0.0" to handle incomplete tags like "v1" or "v1.2".
VERSION_CORE=$(echo "$LATEST_TAG" | sed -e 's/^v//' -e 's/-.*//')
PADDED_VERSION="${VERSION_CORE}.0.0"

MAJOR=$(echo "$PADDED_VERSION" | cut -d. -f1)
MINOR=$(echo "$PADDED_VERSION" | cut -d. -f2)
PATCH=$(echo "$PADDED_VERSION" | cut -d. -f3)

# --- Final Validation ---
# Ensure that the parsed version components are actually numbers.
for part in "$MAJOR" "$MINOR" "$PATCH"; do
  case "$part" in
    ''|*[!0-9]*)
      echo "Error: Could not parse a valid version number from tag '$LATEST_TAG'." >&2
      echo "Please ensure the latest tag is in a format like v1.2.3." >&2
      exit 1
      ;;
  esac
done
# ---

# Prompt user for version bump type
echo "Which part of the version do you want to bump?"
echo "1) major"
echo "2) minor"
echo "3) patch"
while true; do
  printf "Enter your choice (1-3): "
  read choice
  case $choice in
    1)
      MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0; break;;
    2)
      MINOR=$((MINOR + 1)); PATCH=0; break;;
    3)
      PATCH=$((PATCH + 1)); break;;
    *)
      echo "Invalid option. Please enter 1, 2, or 3.";;
  esac
done

# Create the new version tag
NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
echo ""
echo "Calculated new version: $NEW_TAG"
echo ""
echo "To create and push this new tag, run the following commands:"
echo "git tag $NEW_TAG"
echo "git push origin $NEW_TAG"
echo ""
printf "Press [Enter] to continue with the Docker build..."
read _
echo ""

# --- Docker Build Logic ---

docker build \
  --build-arg "MAINTAINER=jamesmortensen" \
  --build-arg "REPO=geckodriver-arm-binaries" \
  --build-arg "GECKODRIVER_VERSION=v0.34.0" \
  --build-arg "ARCH=linux-armv7l" \
  -t "shankershawn/isro-mission-checker:${NEW_TAG}-linux-armv7l" .

echo "Successfully built Docker image: shankershawn/isro-mission-checker:${NEW_TAG}-linux-armv7l"
