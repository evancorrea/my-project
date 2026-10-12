#!/usr/bin/env python3
"""Generate a reproducible synthetic gene-level APA PDUI benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.special import expit, logit


SEED = 42
N_GENES = 100
N_PER_CONDITION = 6
N_AFFECTED = 20
KAPPA = 100


def generate_baselines(rng: np.random.Generator) -> np.ndarray:
    return rng.beta(2, 2, size=N_GENES)


def assign_effects(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    effects = np.zeros(N_GENES)
    affected = np.sort(rng.choice(N_GENES, size=N_AFFECTED, replace=False))
    positive = affected[: N_AFFECTED // 2]
    negative = affected[N_AFFECTED // 2 :]
    magnitudes = rng.uniform(0.7, 1.4, size=N_AFFECTED)
    effects[positive] = magnitudes[: len(positive)]
    effects[negative] = -magnitudes[len(positive) :]
    return effects, affected


def simulate_replicates(
    rng: np.random.Generator, control_mu: np.ndarray, kd_mu: np.ndarray
) -> tuple[pd.DataFrame, pd.DataFrame]:
    sample_ids = [f"Ctrl_{i}" for i in range(1, 7)] + [f"KD_{i}" for i in range(1, 7)]
    rows = []
    for i in range(N_GENES):
        control = rng.beta(control_mu[i] * KAPPA, (1 - control_mu[i]) * KAPPA, size=6)
        knockdown = rng.beta(kd_mu[i] * KAPPA, (1 - kd_mu[i]) * KAPPA, size=6)
        rows.append(np.concatenate((control, knockdown)))
    data = pd.DataFrame(rows, columns=sample_ids)
    data.insert(0, "gene", [f"GENE_{i:03d}" for i in range(1, N_GENES + 1)])
    metadata = pd.DataFrame(
        {"sample_id": sample_ids, "condition": ["control"] * 6 + ["knockdown"] * 6}
    )
    return data, metadata


def make_dataset(seed: int = SEED):
    rng = np.random.default_rng(seed)
    baseline = generate_baselines(rng)
    effects, affected_idx = assign_effects(rng)
    control_mu = baseline
    kd_mu = expit(logit(baseline) + effects)
    data, metadata = simulate_replicates(rng, control_mu, kd_mu)
    affected = np.zeros(N_GENES, dtype=bool)
    affected[affected_idx] = True
    directions = np.where(effects > 0, "positive", np.where(effects < 0, "negative", "null"))
    truth = pd.DataFrame(
        {
            "gene": data["gene"],
            "baseline_expected_pdui": control_mu,
            "knockdown_expected_pdui": kd_mu,
            "true_log_odds_effect": effects,
            "true_delta_pdui": kd_mu - control_mu,
            "affected": affected,
            "effect_direction": directions,
        }
    )
    observed_delta = data.iloc[:, 7:13].mean(axis=1) - data.iloc[:, 1:7].mean(axis=1)
    return data, truth, metadata, observed_delta


def write_outputs(output_dir: Path, seed: int = SEED) -> None:
    agent_dir = output_dir / "agent_environment"
    agent_dir.mkdir(parents=True, exist_ok=True)
    data, truth, metadata, observed_delta = make_dataset(seed)
    agent_path = agent_dir / "apa_pdui_100genes.tsv"
    data.to_csv(agent_path, sep="\t", index=False, float_format="%.10g")
    truth.to_csv(output_dir / "apa_ground_truth_100genes.tsv", sep="\t", index=False, float_format="%.10g")
    metadata.to_csv(output_dir / "apa_sample_metadata.tsv", sep="\t", index=False)
    params = {
        "random_seed": seed,
        "number_of_genes": N_GENES,
        "number_of_samples": 12,
        "samples_per_condition": 6,
        "baseline_beta_distribution": {"alpha": 2, "beta": 2},
        "affected_gene_count": N_AFFECTED,
        "affected_gene_fraction": N_AFFECTED / N_GENES,
        "effect_size_distribution": {"absolute_log_odds": "Uniform(0.7, 1.4)", "signs": "10 positive, 10 negative"},
        "replicate_concentration_kappa": KAPPA,
        "generating_process": "Expected knockdown PDUI is expit(logit(baseline PDUI) + log-odds effect); each replicate is sampled from a beta distribution with mean equal to its condition expectation and concentration kappa.",
        "limitations": [
            "The beta distribution is an illustrative prior over gene-specific baseline PDUI values, not a claim about genome-wide APA usage.",
            "No sequencing reads, read depth, transcript abundance, or APA quantification uncertainty are modeled.",
            "Gene effects are independent, with no shared regulatory mechanisms or gene networks.",
            "Replicate observations are independent conditional on gene-specific expected usage.",
            "There are no batch effects, confounders, or correlations between genes.",
            "True biological effect is defined by latent condition-specific expected PDUI, not observed difference between sample means.",
        ],
    }
    (output_dir / "apa_simulation_parameters.json").write_text(json.dumps(params, indent=2) + "\n")
    baseline = truth["baseline_expected_pdui"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(baseline, bins=15, color="#4C78A8", edgecolor="white")
    ax.set(xlabel="Baseline expected PDUI", ylabel="Genes", title="Baseline expected PDUI")
    fig.tight_layout()
    fig.savefig(output_dir / "baseline_pdui_histogram.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, color in ((False, "#9A9A9A"), (True, "#E45756")):
        mask = truth["affected"].to_numpy() == label
        ax.hist(observed_delta[mask], bins=np.linspace(-0.8, 0.8, 25), alpha=0.7,
                label="Affected" if label else "Null", color=color, edgecolor="white")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set(xlabel="Observed mean ΔPDUI (KD − control)", ylabel="Genes", title="Observed ΔPDUI by true status")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "observed_delta_histogram.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = np.where(truth["affected"], "#E45756", "#9A9A9A")
    ax.scatter(truth["true_delta_pdui"], observed_delta, c=colors, alpha=0.8, edgecolors="white", linewidths=0.4)
    ax.axhline(0, color="black", linewidth=0.7)
    ax.axvline(0, color="black", linewidth=0.7)
    ax.set(xlabel="True ΔPDUI", ylabel="Observed mean ΔPDUI", title="True versus observed ΔPDUI")
    fig.tight_layout()
    fig.savefig(output_dir / "true_vs_observed_delta.png", dpi=160)
    plt.close(fig)

    validate(output_dir, data, truth, metadata, seed)
    npos = int((truth.true_log_odds_effect > 0).sum())
    nneg = int((truth.true_log_odds_effect < 0).sum())
    null_mask = ~truth.affected
    print(f"Genes: {len(truth)} (null={int(null_mask.sum())}, affected={int(truth.affected.sum())})")
    print(f"Effects: positive={npos}, negative={nneg}")
    print(f"Mean baseline PDUI: {baseline.mean():.4f}")
    print(f"Mean absolute true ΔPDUI among affected: {truth.loc[truth.affected, 'true_delta_pdui'].abs().mean():.4f}")
    print(f"Mean absolute observed ΔPDUI among null: {observed_delta[null_mask].abs().mean():.4f}")
    print(f"Wrote run to {output_dir}")


def validate(output_dir: Path, data: pd.DataFrame, truth: pd.DataFrame, metadata: pd.DataFrame, seed: int) -> None:
    assert len(data) == len(truth) == N_GENES
    assert len(metadata) == 12 and data.shape[1] - 1 == 12
    assert int(truth.affected.sum()) == 20
    assert int((truth.true_log_odds_effect > 0).sum()) == 10
    assert int((truth.true_log_odds_effect < 0).sum()) == 10
    assert np.all(truth.loc[~truth.affected, "true_log_odds_effect"] == 0)
    values = data.iloc[:, 1:].to_numpy()
    assert np.all((values >= 0) & (values <= 1))
    regenerated = make_dataset(seed)
    assert data.equals(regenerated[0]) and truth.equals(regenerated[1]) and metadata.equals(regenerated[2])
    saved = pd.read_csv(output_dir / "agent_environment" / "apa_pdui_100genes.tsv", sep="\t")
    assert saved["gene"].equals(data["gene"])
    assert np.allclose(saved.iloc[:, 1:].to_numpy(), values, rtol=1e-9, atol=1e-12)
    assert sorted(p.name for p in (output_dir / "agent_environment").iterdir()) == ["apa_pdui_100genes.tsv"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "runs" / "apa_synthetic_001")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    write_outputs(args.output_dir, args.seed)


if __name__ == "__main__":
    main()
