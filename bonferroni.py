import argparse
import os
import re

import pandas as pd
from statsmodels.stats.multitest import multipletests

#normalize input name to create output one
def csv_basename(filepath):
    match = re.search(r'([^/\\]+)\.csv$', filepath, re.IGNORECASE)
    return match.group(1) if match else os.path.splitext(os.path.basename(filepath))[0]

#apply bonferroni correction on all the multiple hypothesis p-value result
def run_bonferroni(files, output_folder):
    rows = []
    for filepath in files:
        df = pd.read_csv(filepath)
        for p in df["p_value"]:
            rows.append({"source_file": filepath, "p_value": p})

#find how many hypothesis there are
    all_p = [r["p_value"] for r in rows]
    m = len(all_p)

    _, corrected_p, _, _ = multipletests(all_p, method="bonferroni")

    for i, row in enumerate(rows):
        row["p_corrected"] = corrected_p[i]
        row["m"] = m

    result = pd.DataFrame(rows, columns=["source_file", "p_value", "p_corrected", "m"])

    names = "".join(csv_basename(f) for f in files)
    output_filename = f"p_corrected_{names}.csv"

#fall back
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    result.to_csv(output_path, index=False)
    print(f"Results written to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Bonferroni correction for multiple p-values")
    parser.add_argument(
        "--files", nargs="+", required=True, help="Input CSV files containing a p_value column"
    )
    parser.add_argument("--output", required=True, help="Output folder")
    args = parser.parse_args()

    run_bonferroni(args.files, args.output)


if __name__ == "__main__":
    main()



#Code written with AI assistance