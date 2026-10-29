# Health Tracker

Track daily health metrics like water intake, steps, sleep, and weight.

## Usage

```bash
# Log metrics
python health_tracker.py log water 8
python health_tracker.py log steps 10000
python health_tracker.py log sleep 7.5
python health_tracker.py log weight 70

# View today's metrics
python health_tracker.py show

# View specific date
python health_tracker.py show 2026-08-28

# Weekly statistics
python health_tracker.py stats

# Export to CSV
python health_tracker.py export
```

## Metrics Tracked

- Water (glasses)
- Steps
- Sleep (hours)
- Weight (kg)
