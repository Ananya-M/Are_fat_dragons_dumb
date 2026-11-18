import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------- 1. Simulate a crossed design ----------
# 30 dragons, each tested by the same 8 examiners, twice each
rng = np.random.default_rng(1)
n_dragons, n_examiners, n_reps = 30, 8, 2

dragon_effect   = rng.normal(0, 10, n_dragons)    # true dragon SD    = 10  (var 100)
examiner_effect = rng.normal(0, 5,  n_examiners)  # true examiner SD  = 5   (var 25)

rows = []
for dr in range(n_dragons):
    body = rng.normal(0, 1)
    for ex in range(n_examiners):
        for rep in range(n_reps):
            score = (50 + 2 * body
                     + dragon_effect[dr]
                     + examiner_effect[ex]
                     + rng.normal(0, 4))           # true residual SD = 4 (var 16)
            rows.append([f"D{dr}", f"E{ex}", body, score])

d = pd.DataFrame(rows, columns=["dragon", "examiner", "bodyLength", "score"])
print(d.head(10))
print(pd.crosstab(d.dragon, d.examiner).iloc[:5])   # every dragon x every examiner

# ---------- 2. Fit crossed random effects ----------
# statsmodels needs ONE top-level group; put everyone in the same group
# and give BOTH factors as variance components.
d["all"] = 1

m = smf.mixedlm(
    "score ~ bodyLength",
    d,
    groups="all",                       # one big group
    re_formula="0",                     # no intercept for that dummy group
    vc_formula={
        "dragon":   "0 + C(dragon)",    # one random intercept per dragon
        "examiner": "0 + C(examiner)",  # one random intercept per examiner
    },
).fit(reml=True)

print(m.summary())

# ---------- 3. R-style random-effects table ----------
vc = pd.Series(m.vcomp, index=m.model.exog_vc.names)
re = pd.DataFrame({
    "Groups":   list(vc.index) + ["Residual"],
    "Variance": list(vc.values) + [m.scale],
})
re["Std.Dev."] = np.sqrt(re["Variance"])
print(re.round(2).to_string(index=False))
print("True values: dragon 100, examiner 25, residual 16")
