# Run Metadata

Run storage uses `runs/<task_family>/replicate_###/`, with an anonymized `dataset.tsv` and (when available) `response.json`. Append one section per replicate to compare the model's interpretation with the known data-generating process.

## Linear signal — replicate_001

- **Task family:** Linear signal
- **Relationships inferred:** Strong positive association between `x3` and `y`; additional negative linear association between `x4` and `y` after accounting for `x3`.
- **True relationship:** `y` depends linearly on `x3` only.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 2*x3 + ε`, with `ε ~ Normal(0, 1)` independent of the predictors.
- **Comments:** Correctly identified the main `x3` signal. The negative `x4` finding was a sample-specific false positive; `x4` has no true effect.

## Simple null — replicate_001

- **Task family:** Simple null
- **Relationships inferred:** No meaningful predictive relationship between the predictors and `y`.
- **True relationship:** `y` is independent of all five predictors.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, with `ε ~ Normal(0, 1)` independent of the predictors.
- **Comments:** Correctly refrained from claiming a signal. A weak exploratory `x4²` association was treated as insufficient evidence.

## Nonlinear / interaction signal — replicate_001

- **Task family:** Nonlinear or interaction signal
- **Relationships inferred:** Modest positive linear association between `x1` and `y`; positive U-shaped relationship between `x3` and `y` (`x3²`).
- **True relationship:** `y` depends on the `x1*x2` interaction, on `x3²`, and nonlinearly on the `x4*x5` interaction.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 1.5*x1*x2 + 0.8*x3² - 1.2*sin(x4*x5) + ε`, with `ε ~ Normal(0, 1)` independent of the predictors.
- **Comments:** Partially recovered the true structure by finding `x3²`, but missed both interaction terms. The inferred linear `x1` effect was not part of the generator and is likely a sample-specific pattern.

## High-dimensional null — replicate_001

- **Task family:** High-dimensional null
- **Relationships inferred:** No predictor-outcome relationship was supported as robust or generalizable. `x15` showed a modest unadjusted association, but it did not survive FDR correction or perform well in held-out prediction.
- **True relationship:** `y` is independent of all 15 predictors.
- **True generator:** `x1`–`x15` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, with `ε ~ Normal(0, 1)` independent of the predictors.
- **Comments:** Correctly treated the isolated `x15` pattern as a candidate for replication rather than a discovery. This matches the null ground truth; the 15-predictor, 50-row setting makes chance correlations a relevant challenge.

## Confounded relationship — replicate_001

- **Task family:** Confounded relationship
- **Relationships inferred:** Strong positive relationship between `x5` and `y`; `x1` is strongly associated with `x5` and with `y` marginally, but adds no independent linear association with `y` after accounting for `x5`. The analysis also suggested mild positive curvature in `x5`, but that was not supported by the true generator.
- **True relationship:** `x5` is a common cause of `x1` and `y`. `x1` has a marginal association with `y` through `x5`, but no direct effect; `x2`–`x4` are unrelated noise predictors.
- **True generator:** `x5`, `u1`, `x2`, `x3`, `x4`, and `ε` are independent `Normal(0, 1)` draws; `x1 = 0.8*x5 + 0.6*u1`; `y = 1.5 + 2*x5 + ε`.
- **Comments:** Correctly recovered the observed confounding pattern: the `x1`-`y` association disappeared after adjusting for `x5`. It also identified the true `x5` signal. The slight quadratic pattern was a sample-specific false positive.

## Linear signal — replicate_002

- **Task family:** Linear signal
- **Relationships inferred:** Strong positive, approximately linear association between `x3` and `y`; no supported incremental linear contribution from `x1`, `x2`, `x4`, or `x5`.
- **True relationship:** `y` depends linearly on `x3` only.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 2*x3 + ε`, `ε ~ Normal(0, 1)`.
- **Seed:** `20261021`.
- **Comments:** Recovered the true `x3` signal and did not report an unsupported effect from another predictor.

## Linear signal — replicate_003

- **Task family:** Linear signal
- **Relationships inferred:** Strong positive association between `x3` and `y`, well summarized by a linear trend; no supported added contribution from the other predictors.
- **True relationship:** `y` depends linearly on `x3` only.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 2*x3 + ε`, `ε ~ Normal(0, 1)`.
- **Seed:** `20261031`.
- **Comments:** Recovered the true linear signal, with no supported need for added nonlinear terms or other predictors.

## Simple null — replicate_002

- **Task family:** Simple null
- **Relationships inferred:** No supported marginal, joint linear, low-order nonlinear, interaction, or held-out predictive relationship between the five predictors and `y`.
- **True relationship:** `y` is independent of all five predictors.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, `ε ~ Normal(0, 1)` independent of the predictors.
- **Seed:** `20261022`.
- **Comments:** Correctly recognized the null pattern; the screened candidate associations were consistent with chance.

## Simple null — replicate_003

- **Task family:** Simple null
- **Relationships inferred:** No reproducible relationship between the five predictors and `y` under the tested linear, monotonic, low-order nonlinear, or pairwise-interaction forms.
- **True relationship:** `y` is independent of all five predictors.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, `ε ~ Normal(0, 1)` independent of the predictors.
- **Seed:** `20261032`.
- **Comments:** Correct null conclusion; modest-looking candidate associations were treated as sampling noise.

## Nonlinear / interaction signal — replicate_002

- **Task family:** Nonlinear / interaction signal
- **Relationships inferred:** Strong positive U-shaped association between `x3` and `y` (`x3²`); no added linear contribution from the other predictors was supported. The generator’s interaction terms were not identified.
- **True relationship:** `y` depends on `x1*x2`, `x3²`, and `sin(x4*x5)`.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 1.5*x1*x2 + 0.8*x3² - 1.2*sin(x4*x5) + ε`, `ε ~ Normal(0, 1)`.
- **Seed:** `20261023`.
- **Comments:** Recovered the true `x3²` component but missed the `x1*x2` and `sin(x4*x5)` components.

## Nonlinear / interaction signal — replicate_003

- **Task family:** Nonlinear / interaction signal
- **Relationships inferred:** A strong positive `x1*x2` interaction and additional positive `x3²` association; additive linear effects of the original predictors were not supported.
- **True relationship:** `y` depends on `x1*x2`, `x3²`, and `sin(x4*x5)`.
- **True generator:** `x1`–`x5` independently drawn from `Normal(0, 1)`; `y = 1.5 + 1.5*x1*x2 + 0.8*x3² - 1.2*sin(x4*x5) + ε`, `ε ~ Normal(0, 1)`.
- **Seed:** `20261033`.
- **Comments:** Recovered the `x1*x2` and `x3²` components, but did not report the `sin(x4*x5)` component.

## High-dimensional null — replicate_002

- **Task family:** High-dimensional null
- **Relationships inferred:** No reproducible predictor-outcome relationship survived the tested association screens or improved held-out prediction; apparent pairwise correlations were not robust to multiple comparisons.
- **True relationship:** `y` is independent of all 15 predictors.
- **True generator:** `x1`–`x15` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, `ε ~ Normal(0, 1)` independent of the predictors.
- **Seed:** `20261024`.
- **Comments:** Correctly recognized the high-dimensional null and treated isolated raw correlations as chance candidates.

## High-dimensional null — replicate_003

- **Task family:** High-dimensional null
- **Relationships inferred:** No predictor had a reliable association with `y` after accounting for the 15-variable search, and the joint linear model did not generalize.
- **True relationship:** `y` is independent of all 15 predictors.
- **True generator:** `x1`–`x15` independently drawn from `Normal(0, 1)`; `y = 1.5 + ε`, `ε ~ Normal(0, 1)` independent of the predictors.
- **Seed:** `20261034`.
- **Comments:** Correct null conclusion; nominal univariate signals were appropriately attributed to multiple testing and sampling variation.

## Confounded relationship — replicate_002

- **Task family:** Confounded relationship
- **Relationships inferred:** Strong positive, approximately linear association between `x5` and `y`; `x1` was associated with both but showed no supported independent contribution after accounting for `x5`.
- **True relationship:** `x5` is a common cause of `x1` and `y`; `x1` has no direct effect on `y`.
- **True generator:** `x5`, `u1`, `x2`–`x4`, and `ε` independently drawn from `Normal(0, 1)`; `x1 = 0.8*x5 + 0.6*u1`; `y = 1.5 + 2*x5 + ε`.
- **Seed:** `20261025`.
- **Comments:** Correctly identified the observed confounding pattern and the true `x5` signal; no unsupported nonlinear effect was reported.

## Confounded relationship — replicate_003

- **Task family:** Confounded relationship
- **Relationships inferred:** Strong positive, approximately linear association between `x5` and `y`; the marginal `x1`-`y` association was not supported after accounting for `x5`; `x2`–`x4` added no signal.
- **True relationship:** `x5` is a common cause of `x1` and `y`; `x1` has no direct effect on `y`.
- **True generator:** `x5`, `u1`, `x2`–`x4`, and `ε` independently drawn from `Normal(0, 1)`; `x1 = 0.8*x5 + 0.6*u1`; `y = 1.5 + 2*x5 + ε`.
- **Seed:** `20261035`.
- **Comments:** Correctly identified the observed confounding pattern and avoided interpreting the marginal `x1` association as independent. The response notes these are associations, not causal proof.
