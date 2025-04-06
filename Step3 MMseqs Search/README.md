# Step 3: MMseqs Search

## Overview
This step, we use the latest version of [MMseqs2](https://github.com/soedinglab/MMseqs2) to search through sequence database, in order to get expand the discovered enzyme database

Recommended databases:
- NCBI no redundant database (NR)
- MEER (this is a private deep-sea sequencing database)

## Requirements

What you need to prepare before you submit the job
- MMseqs module (already installed on server) or MMseqs software installed
- Database: NR or MEER or etc. First downloading NR database can refer to the MMseqs2 document
- Input file: xxx_foldseek.fasta

## Submit the job
submit the mmseqs job `sub_mmseqs.pbs` using the `qsub` command:

```bash
qsub sub_mmseqs.pbs
```

Some file name adjustments needs to be done.

## Command One-by-one

Command 1: use `mmseqs` to search through the NCBI NR or MEER database

```bash
mmseqs easy-search protein_foldseek.fasta /global/lhshare/mmseqs_database/MEER/MEER protein_MEER.tsv --format-output "query,target,pident,fident,nident,alnlen,bits,tseq,evalue" tmp --threads 96 --num-iterations 2 --max-seqs 2500 --search-type 1
```

Command 2: use `tsv2fasta.py` to convert the `.tsv` file to a `.fasta` file. This code has no package requirement

```bash
python tsv2fasta.py protein_MEER.tsv protein_MEER.fasta
```



