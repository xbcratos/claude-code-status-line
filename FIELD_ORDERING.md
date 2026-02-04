# Field Ordering Guide

The Claude Code Statusline Tool allows you to customize the order in which fields appear.

## How Field Ordering Works

Fields are grouped into semantic lines, but **within each line, the order respects your `field_order` configuration**:

### Line Assignment

**Line 1 (Identity):**
- `current_dir` - Current directory
- `git_branch` - Git branch name
- `model` - Model name
- `version` - Claude Code version
- `output_style` - Output style name

**Line 2 (Status):**
- `context_remaining` - Context window remaining (compact mode)
- `context_remaining` + `duration` - Both shown (large mode)

**Line 3 (Metrics):**
- `cost` - Total cost
- `tokens` - Total tokens
- `duration` - Session duration (compact mode)
- `lines_changed` - Lines modified

## Default Field Order

```json
{
  "field_order": [
    "current_dir",
    "git_branch",
    "model",
    "version",
    "context_remaining",
    "tokens",
    "cost",
    "duration",
    "lines_changed",
    "output_style"
  ]
}
```

**Output:**
```
📁 my-project  🌿 main  🤖 Sonnet 4  📟 v1.0.85
🧠 Context Remaining: 95% [=========-]
📊 15000 tok (1250 tpm)  💰 $2.48 ($12.40/h)
```

## Custom Ordering Examples

### Example 1: Model First

Put model information before location:

```json
{
  "field_order": [
    "model",
    "version",
    "git_branch",
    "current_dir",
    "context_remaining",
    "cost",
    "tokens"
  ]
}
```

**Output:**
```
🤖 Sonnet 4  📟 v1.0.85  🌿 main  📁 my-project
🧠 Context Remaining: 95% [=========-]
💰 $2.48 ($12.40/h)  📊 15000 tok (1250 tpm)
```

### Example 2: Cost First

Prioritize cost information:

```json
{
  "field_order": [
    "current_dir",
    "git_branch",
    "model",
    "version",
    "context_remaining",
    "cost",
    "tokens"
  ]
}
```

**Output:**
```
📁 my-project  🌿 main  🤖 Sonnet 4  📟 v1.0.85
🧠 Context Remaining: 95% [=========-]
💰 $2.48 ($12.40/h)  📊 15000 tok (1250 tpm)
```

## Reordering via Configuration Tool

1. Run: `claude-statusline-config`
2. Select: **Option 5 - Reorder Fields**
3. View current order with numbers
4. Enter two numbers to swap positions (e.g., `1 3`)
5. Select: **Option 10 - Save and Exit**

## Manual Configuration

Edit `~/.claude-code-statusline/config.json`:

```json
{
  "field_order": ["model", "version", "current_dir", "git_branch", ...]
}
```

**Note:** You control the order within each line, but cannot move fields between lines 1, 2, and 3.
