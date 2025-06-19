import io
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate value and effort charts from CSV data.')
    parser.add_argument('-i', '--input', required=True,
                        help='Input CSV file path.')
    parser.add_argument('-o', '--output', default='charts',
                        help='Output directory for charts.')
    return parser.parse_args()


def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    processed_data = []
    for column in df.columns:
        parts = column.split(' - ')
        if len(parts) == 2:
            field, metric = parts
            for value in df[column]:
                processed_data.append({
                    'Field': field.strip(),
                    'Metric': metric.strip(),
                    'Score': value
                })

    tidy_df = pd.DataFrame(processed_data)

    value_df = tidy_df[tidy_df['Metric'] == 'Value']
    effort_df = tidy_df[tidy_df['Metric'] == 'Effort/Complexity']

    avg_value = value_df.groupby('Field')['Score'].mean()
    avg_effort = effort_df.groupby('Field')['Score'].mean()

    combined_df = pd.merge(avg_value.rename('Value'), avg_effort.rename(
        'Effort'), left_index=True, right_index=True)

    return combined_df


def create_and_save_charts(chart_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(10, 8))
    plt.scatter(chart_data['Effort'], chart_data['Value'],
                s=100, alpha=0.7, edgecolor='black')

    for field, row in chart_data.iterrows():
        plt.text(row['Effort'] + 0.05, row['Value'], field, fontsize=9)

    plt.axvline(x=chart_data['Effort'].mean(), color='grey', linestyle='--')
    plt.axhline(y=chart_data['Value'].mean(), color='grey', linestyle='--')

    plt.title('Value vs. Effort Quadrant Chart', fontsize=16)
    plt.xlabel('Effort / Complexity Score', fontsize=12)
    plt.ylabel('Value Score', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    quadrant_chart_path = os.path.join(output_dir, 'quadrant_chart.png')
    plt.savefig(quadrant_chart_path)
    plt.close()
    print(f"Saved quadrant chart to {quadrant_chart_path}")

    chart_data.sort_values('Value', ascending=False).plot(
        kind='bar',
        figsize=(14, 7),
        color={'Value': 'skyblue', 'Effort': 'salmon'},
        edgecolor='black'
    )
    plt.title('Value and Effort/Complexity per Field', fontsize=16)
    plt.ylabel('Average Score', fontsize=12)
    plt.xlabel('Field', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    grouped_chart_path = os.path.join(output_dir, 'grouped_bar_chart.png')
    plt.savefig(grouped_chart_path)
    plt.close()
    print(f"Saved grouped bar chart to {grouped_chart_path}")


def main():
    args = parse_arguments()
    chart_data = load_and_process_data(args.input)
    create_and_save_charts(chart_data, args.output)


if __name__ == "__main__":
    main()
