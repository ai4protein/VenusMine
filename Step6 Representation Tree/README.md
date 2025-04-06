# Step 6: Representation Tree

Follow the steps in `deep_tree.ipynb`

Requirement:
- matplotlib v3.7.1
- numpy v1.24.3
- scipy v1.10.1
- pandas v1.5.3

Acutally, these packages are broadly available in conda environments, and almost all versions of these packages should work for this notebook.

## Data preperation

- `refseq.pkl` is the ProstT5 representation from step 5, there sequences are reference sequences, which has confirmed activity.
- `result.pkl` is the ProstT5 representation from step 5, sequences are from step 4 mmseqs clusters
- `ec.pkl` is ProstT5 representation from step 5, sequences are from SwissProt with confirmed EC number
- `ec_dataset.csv` contains the information for `ec.pkl`, this file is available at https://zenodo.org/records/15163501

We provide the fasta files in step 5 `sequence` folder to calculated `ec.pkl` and `refseq.pkl` used in our PETase discovery study. If you want to do for another enzyme, you should provide new `refseq.pkl`, but you can keep the `ec.pkl`

The result will have 2 files:
- A repr. tree figure (different repr. tree clusters are colored differently)
- A `.tsv` file with sequence information included, you can find the sequence name and repr. tree cluster of them
