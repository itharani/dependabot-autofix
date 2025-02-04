#!/bin/bash
set -e

echo "Detecting package manager..."

if [ -f "package.json" ]; then
  echo "Node.js project detected"
  npm install -g npm-check-updates
  ncu -u && npm install

elif [ -f "requirements.txt" ]; then
  echo "Python project detected"
  pip install --upgrade pip
  pip install --upgrade -r requirements.txt

elif [ -f "pyproject.toml" ]; then
  echo "Poetry-based Python project detected"
  pip install --upgrade poetry
  poetry update

elif [ -f "Cargo.toml" ]; then
  echo "Rust project detected"
  cargo update

elif [ -f "pom.xml" ]; then
  echo "Maven (Java) project detected"
  mvn versions:update-properties

elif [ -f "build.gradle" ]; then
  echo "Gradle (Java) project detected"
  gradle dependencies --write-locks

elif [ -f "go.mod" ]; then
  echo "Go project detected"
  go get -u ./...

elif [ -f "composer.json" ]; then
  echo "PHP project detected"
  composer update --no-interaction

elif [ -f "Gemfile" ]; then
  echo "Ruby project detected"
  bundle update

elif [ -f "mix.exs" ]; then
  echo "Elixir project detected"
  mix deps.update --all

elif [ -f "CMakeLists.txt" ]; then
  echo "C++ CMake project detected"
  cmake --fresh-build

else
  echo "No supported package manager found. Exiting."
  exit 0
fi

echo "Dependency updates completed."
