# Reproduce the APA dataset

From the repository root, run:

```bash
python APA_eval/generate_apa_dataset.py
```

This uses the default random seed (`42`) and writes the dataset and supporting files to `APA_eval/runs/apa_synthetic_001/`. The agent-visible TSV is in its `agent_environment/` subdirectory. Python needs NumPy, pandas, SciPy, and Matplotlib installed.

## Data model

The generator draws each gene's baseline PDUI from Beta(2, 2). Twenty genes receive log-odds effects under knockdown (10 positive and 10 negative); the other 80 are null. It simulates six control and six knockdown replicates per gene from beta distributions centered on the condition-specific expected PDUIs, using concentration `kappa=100`.

## Files

- `APA_eval/generate_apa_dataset.py`: generator.
- `APA_eval/runs/apa_synthetic_001/agent_environment/apa_pdui_100genes.tsv`: dataset provided to the agent.
- `APA_eval/runs/apa_synthetic_001/apa_ground_truth_100genes.tsv`: private gene-level effects and expected PDUIs.
- `APA_eval/runs/apa_synthetic_001/apa_sample_metadata.tsv` and `apa_simulation_parameters.json`: sample conditions and simulation settings.
- `APA_eval/runs/apa_synthetic_001/*.png`: diagnostic plots.

This is a simplified synthetic statistical model and does not represent real biological data.
