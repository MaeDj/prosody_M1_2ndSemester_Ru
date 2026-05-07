

Statistical analysis pipeline

## Overview

This algorithm computes a **p-value** for a predefined hypothesis given two groups of data. It automatically selects the appropriate statistical test based on whether the data are paired and whether they follow a normal distribution.

## Input

- Two CSV files, one per group (paths provided by the user)
- The name of the column to compare in each CSV file 
- A boolean parameter `paired` indicating whether the two groups are paired samples
- The path to the output folder where results will be written

## Statistical Decision Pipeline

The algorithm first runs a **Shapiro-Wilk normality test** on each group, then selects the test as follows:

| Paired | Normally distributed | Test applied      |
|--------|----------------------|-------------------|
| Yes    | Yes                  | Paired t-test     |
| Yes    | No                   | Wilcoxon          |
| No     | Yes                  | ANOVA             |
| No     | No                   | Mann-Whitney U    |

## Output

Results are written to `<output_folder>/p_value_<name1>_<name2>_<column_name>.csv` containing:

- The **p-value** resulting from the selected statistical test
- The test statistic
- The name of the test that was applied
- The normality test results (Shapiro-Wilk statistic and p-value for each group)

## Usage

```
python main.py --file1 group1.csv --file2 group2.csv --col1 <column_name_in_file1> --col2 <column_name_in_file2> --paired <true|false> --output <output_folder> [--alpha_shapiro 0.05]
```

| Argument | Required | Description |
|---------------|----------|-------------|
| `--file1` | yes | Path to the first group CSV file |
| `--file2` | yes | Path to the second group CSV file |
| `--col1` | yes | Column name to analyse in `file1` |
| `--col2` | yes | Column name to analyse in `file2` |
| `--paired` | yes | `true` if samples are paired, `false` otherwise |
| `--output` | yes | Folder where the result CSV will be written (created if absent) |
| `--alpha_shapiro` | no | Significance threshold for the Shapiro-Wilk test (default: `0.05`) |

---

## Bonferroni Correction

A second function aggregates results from multiple hypothesis tests and applies a **Bonferroni correction** to control for the family-wise error rate across all comparisons.

### Input

- Multiple CSV files, each containing a `p_value` column (e.g. output files from the statistical test function above)

### How it works

1. Reads the `p_value` column from every input CSV
2. Counts the total number of p-values collected across all files — this count is used as the number of hypotheses *m*
3. Applies the Bonferroni correction using `statsmodels.stats.multitest.multipletests` with `method='bonferroni'`
4. Writes all corrected p-values to a new CSV file

### Output

Results are written to `<output_folder>/p_corrected_<names>_<column_name>.csv` (where `<names>` is the concatenation of the input basenames), containing:

- `source_file` — the input file the p-value came from
- `p_value` — the original p-value
- `p_corrected` — the Bonferroni-corrected p-value (`p_value * m`, capped at 1.0)
- `m` — the total number of hypotheses used for the correction

### Usage

```
python bonferroni.py --files result1.csv result2.csv result3.csv --output <output_folder>
```

| Argument | Required | Description |
|-----------|----------|-------------|
| `--files` | yes | One or more CSV files each containing a `p_value` column (e.g. outputs from `main.py`) |
| `--output` | yes | Folder where the corrected result CSV will be written (created if absent) |

---

## Dependencies

- Python 3
- `scipy` — Shapiro-Wilk, t-test, ANOVA, Wilcoxon, Mann-Whitney
- `statsmodels` — Bonferroni correction (`multipletests`)
- `pandas` — CSV loading and writing
