# SBP Insight

**An Analysis of Organizational Behavior and Dynamics: A Case Study of the State Bank of Pakistan (SBP)**

Organizational Behavior · Group 5 · Department of Data Science, Dawood University of Engineering & Technology, Karachi · Batch 25/F, Section C

| Name | Roll number |
|---|---|
| Muhammad Abdul Rahman Khan | 25F-DS-106 |
| Muhammad Huzaifa Shamsi | 25F-DS-135 |
| Basit Mirza | 25F-DS-140 |
| Muhammad Hashir | 25F-DS-152 |

## What is inside

An interactive Streamlit app that presents our OB case study of SBP:

| Tab | What it shows |
|---|---|
| Overview | Vision, mission, six core values, the six goals of SBP Vision 2028 |
| Structure | Interactive sunburst of SBP's functional groups and departments; Board, MPC and Executive Committee; structure through OB models |
| Culture | Hofstede radar for Pakistan; Schein's three levels of culture at SBP |
| Communication | SBP's communication channels and a **text-analytics dashboard** of Monetary Policy Statements (readability, tone vs. policy rate, top words by governor era) |
| Leadership | Timeline of every SBP governor since 1948; leadership-style assessment |
| Power & Conflict | Stakeholder power–interest grid; real cases (2022–2026) filtered by Thomas–Kilmann conflict mode; French & Raven power bases |
| SWOT | SWOT matrix and recommendations |

## Data Science part

`mps_nlp.csv` holds one row per SBP Monetary Policy Statement: date, governor, word count, Flesch–Kincaid grade, Flesch reading ease, counts of hawkish and dovish words, net tone and the policy rate mentioned in the decision sentence. Text was extracted from the PDF statements published on sbp.org.pk.

- **Readability** = Flesch–Kincaid grade (school grade needed to understand the text).
- **Net tone** = (hawkish − dovish words) ÷ (hawkish + dovish words), using a small central-bank word list (for example *tightening, inflationary pressures* vs *easing, support growth*).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a public GitHub repository.
2. On share.streamlit.io choose **New app**, pick the repository, branch `main` and file `app.py`.

## Sources

SBP website and Strategic Plan 2023–28, SBP Act 1956 (amended 2022), Dawn, Express Tribune, Business Recorder, Profit and ProPakistani. This is secondary research; statements about SBP's internal culture are the group's own analysis.
