#!/bin/sh

# Exit on error
set -e

# --- Versioning Logic ---

# Get the latest git tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current latest tag is: $LATEST_TAG"

# Parse the version numbers using POSIX-compliant tools
VERSION_NO_V=$(echo "$LATEST_TAG" | sed 's/v//')
MAJOR=$(echo "$VERSION_NO_V" | cut -d. -f1)
MINOR=$(echo "$VERSION_NO_V" | cut -d. -f2)
PATCH=$(echo "$VERSION_NO_V" | cut -d. -f3)

# Prompt user for version bump type
echo "Which part of the version do you want to bump?"
echo "1) major"
echo "2) minor"
echo "3) patch"
while true; do
  read -p "Enter your choice (1-3): " choice
  case $choice in
    1)
      MAJOR=$((MAJOR + 1))
      MINOR=0
      PATCH=0
      break
      ;;
    2)
      MINOR=$((MINOR + 1))
      PATCH=0
      break
      ;;
    3)
      PATCH=$((PATCH + 1))
      break
      ;;
    *)
      echo "Invalid option. Please enter 1, 2, or 3."
      ;;
  esac
done

# Create the new version tag
NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
echo "Calculated new version: $NEW_TAG"
echo ""
echo "To create and push this new tag, run the following commands:"
echo "git tag $NEW_TAG"
echo "git push origin $NEW_TAG"
echo ""
read -p "Press [Enter] to continue with the Docker build..."

# --- Docker Build Logic ---

# Docker build command
docker build \
  --build-arg "MAINTAINER=jamesmortensen" \
  --build-arg "REPO=geckodriver-arm-binaries" \
  --build-arg "GECKODRIVER_VERSION=v0.34.0" \
  --build-arg "ARCH=linux-armv7l" \
  -t "shankershawn/isro-mission-checker:${NEW_TAG}-linux-armv7l" .

echo "Successfully built Docker image: shankershawn/isro-mission-checker:${NEW_TAG}-linux-armv7l"
