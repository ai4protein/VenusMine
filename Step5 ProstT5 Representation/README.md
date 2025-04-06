# Step 5: ProstT5 Representation

## Installation

Create and install packages via conda (recommended)
- This will help you create an environment named `prostt5`

```bash
conda env create -f environment.yml
```

Install packages one-by-one (not recommended)

```bash
conda install pytorch -c pytorch   # for CPU
conda install pytorch pytorch-cuda -c pytorch -c nvidia     # for GPU
conda install transformers
conda install -c conda-forge sentencepiece
conda install -c conda-forge protobuf
```

User might need to download ProstT5 parameters, it may takes several minutes. ProstT5 version and documentation can be found in [Hugging Face](https://huggingface.co/Rostlab/ProstT5)

For EC dataset, you need to also calculate the representation of`ec_dataset.fasta`, which is available at https://zenodo.org/records/15163501
