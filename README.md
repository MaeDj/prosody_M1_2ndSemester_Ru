# French Vowel Perception Study — Statistical Analysis Pipeline

**Authors**: Alexandre CHOPLIN, Maé DUGOUA-JACQUES
**Supervisor**: S. Ruvoletto
**Course**: Prosody — M1 2nd Semester

---

## Research Purpose

This project investigates whether the **perception of French vowels is the same for native and non-native speakers** of French. It is a phonetics/prosody study centred on auditory discrimination.

Two features were measured to compare the two groups:

- **Accuracy** — number of mistakes made across the test
- **Reaction time** — measured in milliseconds

A secondary axis of research tested the **robustness** of the main hypothesis by studying the influence of the following modalities on the native/non-native gap:

| Modality | Sub-groups |
| --- | --- |
| Device | Headphones / Speakers |
| French level | Lower / Higher |
| French listening rate | Lower / Higher |
| French years of practice | Fewer / More |
| Gender | Male or non-binary / Female |
| Reaction time | Lower score / Higher score |
| Nasality | Nasal vowels / Oral vowels |
| Sex of the speaker | Male / Female |

---

## Experiment Design

### Participants

33 participants in total:

- **17 native** French speakers
- **16 non-native** French speakers from diverse language backgrounds (English ×3, Italian ×3, Portuguese, Romanian, Pulaar, Slovenian, Korean, Arabic, German, Turkish, Slovak)

Age range: 20–30 years old.

### Task

A **discrimination task**: participants listened to 144 pairs of made-up syllables and judged whether each pair was the *same* word or *two different* words. The test took approximately 5–10 minutes.

- Trial order was **randomised** to prevent priming effects
- A random delay was added between the two words of each pair to counteract rhythm-based guessing
- Participants completed one **practice trial** before the main test
- Progress tracking was displayed to keep participants engaged
- The test was hosted on a website so participants could take it at their own pace

### Material

36 stimuli were recorded, covering both **nasal** (e.g. /bɑ̃/, /dɑ̃/, /gɑ̃/) and **oral** (e.g. /ba/, /da/, /ga/) French vowels, pronounced by:

- A **male voice** (Alexandre)
- A **female voice** (Mae)

Each stimulus pair was recorded with consistent audio processing (`samplerate=44100`, `channels=1`), trimmed to the same length, and background noise was reduced. Pairs were generated using a Python script that groups stimuli by consonantal structure (onset and coda) to ensure phonological relevance.

This yielded **144 pairs** total (36 different-sound pairs + 36 same-sound pairs, per voice).

---

## Statistical Pipeline

For each hypothesis, the pipeline automatically selects the appropriate statistical test based on data distribution:

| Paired | Normally distributed | Test applied |
| --- | --- | --- |
| Yes | Yes | Paired t-test |
| Yes | No | Wilcoxon |
| No | Yes | ANOVA |
| No | No | Mann-Whitney U |

Normality is assessed with the **Shapiro-Wilk test**. A **Bonferroni correction** is then applied across all p-values to control the family-wise error rate.

In total, **24 groups** were studied: 2 global groups (all natives vs. all non-natives) + 8 modalities × 2 sub-groups × 2 features, minus 6 cases where the global native group substituted an undefined sub-group.

See [`README_stats.md`](README_stats.md) for full documentation of the statistical scripts (`main.py`, `bonferroni.py`).

---

## Key Results

### Main hypothesis

> H0: Perception of French vowels is the same for native and non-native speakers.

| Feature | p-value | p-corrected | Decision |
| --- | --- | --- | --- |
| Accuracy | 0.1509 | 0.3019 | Rejected |
| Reaction time | 0.0525 | 0.1050 | Rejected |

### Robustness hypothesis

> H0: The native/non-native difference holds independently of other modalities.

Both accuracy and reaction time sub-hypotheses were **rejected** overall, meaning the modalities do influence the observed gap — though some specific sub-sub-hypotheses were accepted (e.g. reaction time difference between group 2 and the global group: p-corrected = 0.0472, accepted).

---

## Project Structure

```
.
├── main.py                  # Statistical test pipeline (p-value computation)
├── bonferroni.py            # Bonferroni correction across multiple tests
├── classify_participants.py # Participant group classification
├── data/                    # Input CSV files and p-value results
├── graphs/                  # Generated visualisations
├── README_stats.md          # Technical documentation of the statistical scripts
└── report_prosody_ruvoletto_CHOPLIN_DUGOUA.pdf  # Full report
```

---

## Dependencies

- Python 3
- `scipy` — Shapiro-Wilk, t-test, ANOVA, Wilcoxon, Mann-Whitney U
- `statsmodels` — Bonferroni correction
- `pandas` — CSV I/O