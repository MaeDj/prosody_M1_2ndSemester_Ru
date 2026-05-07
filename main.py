import argparse
import os
import re

import pandas as pd
from scipy import stats

#Normalize csv name to be reused as in the name of the output file
def csv_basename(filepath):
    match = re.search(r'([^/\\]+)\.csv$', filepath, re.IGNORECASE)
    return match.group(1) if match else os.path.splitext(os.path.basename(filepath))[0]

#Make the statistic analysis between 2 groups, will be run multiple time for each hypothesis

def run_analysis(file1, file2, col1, col2, paired, output_folder, alpha_shapiro=0.05):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)


#drop NA but not null values. NA cannot be processed
    data1 = df1[col1].dropna().values
    data2 = df2[col2].dropna().values

    shapiro_stat1, shapiro_p1 = stats.shapiro(data1)
    shapiro_stat2, shapiro_p2 = stats.shapiro(data2)
#always supposed to be "both normal" but in case
    both_normal = (shapiro_p1 > alpha_shapiro) and (shapiro_p2 > alpha_shapiro)

    if paired and both_normal:
        test_name = "paired t-test"
        test_stat, p_value = stats.ttest_rel(data1, data2)
    elif paired and not both_normal:
        test_name = "Wilcoxon"
        test_stat, p_value = stats.wilcoxon(data1, data2)
    elif not paired and both_normal:
        test_name = "ANOVA"
        test_stat, p_value = stats.f_oneway(data1, data2)
    else:
        test_name = "Mann-Whitney U"
        test_stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')

    result = pd.DataFrame([{
        "test": test_name,
        "p_value": p_value,
        "test_statistic": test_stat,
        "shapiro_stat_group1": shapiro_stat1,
        "shapiro_p_group1": shapiro_p1,
        "shapiro_stat_group2": shapiro_stat2,
        "shapiro_p_group2": shapiro_p2,
    }])

    name1 = csv_basename(file1)
    name2 = csv_basename(file2)
    output_filename = f"p_value_{name1}_{name2}_{col1}.csv"

#fall back if the output directory given does not exist
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    result.to_csv(output_path, index=False)
    print(f"Results written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Statistical test selection pipeline")
    parser.add_argument("--file1", required=True, help="Path to first CSV file")
    parser.add_argument("--file2", required=True, help="Path to second CSV file")
    parser.add_argument("--col1", required=True, help="Column name in file1")
    parser.add_argument("--col2", required=True, help="Column name in file2")
    parser.add_argument(
        "--paired",
        required=True,
        type=lambda x: x.lower() == "true",
        help="Paired samples (true/false)",
    )
    parser.add_argument("--output", required=True, help="Output folder")
    parser.add_argument(
        "--alpha_shapiro",
        type=float,
        default=0.05,
        help="Significance threshold for the Shapiro-Wilk normality test (default: 0.05)",
    )
    args = parser.parse_args()

    run_analysis(
        args.file1,
        args.file2,
        args.col1,
        args.col2,
        args.paired,
        args.output,
        args.alpha_shapiro,
    )


if __name__ == "__main__":
    main()

#Code written with AI assistance