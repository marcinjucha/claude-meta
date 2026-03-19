#!/bin/bash
input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "Unknown model"')

# effort_level is not part of the standard status line JSON; read from settings as the source of truth
# null/missing effortLevel means Claude Code is running at max (uncapped) effort
effort=$(jq -r '.effortLevel // "max"' /Users/marcinjucha/.claude/settings.json 2>/dev/null)
effort_part=" | ${effort:-max}"

total_in=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
total_out=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')

# Model-aware pricing ($/M tokens)
model_id=$(echo "$input" | jq -r '.model.id // ""')
case "$model_id" in
    *opus*)   in_rate=15;  out_rate=75 ;;
    *haiku*)  in_rate=0.80; out_rate=4 ;;
    *)        in_rate=3;   out_rate=15 ;;  # default: Sonnet
esac
cost=$(echo "$total_in $total_out $in_rate $out_rate" | awk '{printf "%.3f", ($1 / 1000000 * $3) + ($2 / 1000000 * $4)}')

used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$used_pct" ]; then
    ctx=$(printf "%.0f%%" "$used_pct")
    ctx_part=" | ctx: ${ctx}"
else
    ctx_part=""
fi

printf "%s%s | $%s%s" "$model" "$effort_part" "$cost" "$ctx_part"
