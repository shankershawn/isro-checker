#!/bin/bash

# Exit on error
set -e

# --- Versioning Logic ---

# Get the latest git tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "Current latest tag is: $LATEST_TAG"

# Parse the version numbers
IFS='.' read -ra VERSION_PARTS <<< "${LATEST_TAG//v/}"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Prompt user for version bump type
echo "Which part of the version do you want to bump?"
select BUMP_TYPE in "major" "minor" "patch"; do
  case $BUMP_TYPE in
    major)
      MAJOR=$((MAJOR + 1))
      MINOR=0
      PATCH=0
      break
      ;;
    minor)
      MINOR=$((MINOR + 1))
      PATCH=0
      break
      ;;
    patch)
      PATCH=$((PATCH + 1))
      break
      ;;
    *)
      echo "Invalid option. Please choose 1, 2, or 3."
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
  -t shankershawn/isro-mission-checker:"${NEW_TAG}-linux-armv7l" .

echo "Successfully built Docker image: shankershawn/isro-mission-checker:${NEW_TAG}-linux-armv7l"
