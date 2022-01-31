#!/usr/bin/env bash

PASSWORD_LENGTH="${1:-12}"
REGION="${2:-us-east-1}"

aws secretsmanager get-random-password \
  --password-length $PASSWORD_LENGTH \
  --require-each-included-type \
  --region $REGION \
  --output 'text' \
  --no-cli-pager
