# create_charts.py

Generates value vs effort visualization charts from CSV data.

## Usage

```bash
python create_charts.py -i data.csv -o charts/
```

## Arguments

- `-i, --input`: Input CSV file (required)
- `-o, --output`: Output directory (default: charts)

## Output

- `quadrant_chart.png`: Scatter plot with value/effort quadrants
- `grouped_bar_chart.png`: Bar chart comparing value and effort scores

## Data Format

CSV columns should follow pattern: `Field - Metric` where Metric is either "Value" or "Effort/Complexity".