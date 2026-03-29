#!/bin/bash
# Validates SQL queries to allow only SELECT (read-only operations)
# Used as PreToolUse hook example in agent-creator skill

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Skip validation if no command
if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
# INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, REPLACE, MERGE
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2  # Exit code 2 blocks the operation
fi

# Allow all other commands (SELECT queries)
exit 0
