# Are fat dragons dumb? Linear mixed models in Python

A Python (statsmodels) walk-through of the Coding Club tutorial
**[Introduction to linear mixed models](https://ourcodingclub.github.io/tutorials/mixed-models/)**,
which is where I practised this material. The tutorial is written in R (`lme4`). Each notebook shows the tutorial's
R code next to the Python equivalent.

The question, from the tutorial: does a dragon's body length affect its intelligence test score, once you account
for dragons being sampled from different mountain ranges and sites?

## Notebooks

| Notebook | Tutorial sections |
|---|---|
| `01_explore_and_linear_models.ipynb` | Explore the data, fit all data in one analysis, run multiple analyses, modify the current model |
| `02_mixed_effects_models.ipynb` | First mixed model, crossed vs nested random effects, the correct nested model, random slopes |
| `03_presenting_results_and_model_selection.ipynb` | Presenting model results (plots and tables), p-values and model selection |
| `crossed_example.py` | Extra: a simulated **crossed** design (30 dragons x 8 examiners), to contrast with the nested one |

## R to Python cheat sheet

| lme4 (R) | statsmodels (Python) |
|---|---|
| `lm(y ~ x, data)` | `smf.ols("y ~ x", data).fit()` |
| `lmer(y ~ x + (1 \| g), data)` | `smf.mixedlm("y ~ x", data, groups=data["g"]).fit()` |
| `(1 + x \| g)` (random slope) | `groups="g", re_formula="~x"` |
| `(1 \| g:h)` (nested) | `vc_formula={"h": "0 + C(h)"}` |
| `(1 \| a) + (1 \| b)` (crossed) | one group for everyone + `vc_formula` for `a` and `b` |
| `ranef(m)` | `m.random_effects` |

## Data

`dragons.csv` is the dragons dataset from the Coding Club tutorial (a made-up dataset created for teaching).

## Running

```bash
pip install pandas numpy matplotlib statsmodels scipy
jupyter lab
```

## Credit

Tutorial and dataset: [Coding Club, "Introduction to linear mixed models"](https://ourcodingclub.github.io/tutorials/mixed-models/).
This repo is my Python translation, written for practice.
