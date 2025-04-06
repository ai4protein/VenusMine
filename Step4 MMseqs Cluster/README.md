# Step 4: MMseqs Cluster

Since there might be too much sequence after step 3, we tend to use MMseqs2 to cluster similar sequences

## Commands

First, move the searched result `.fasta` file in step 3 in this directory (you can create one)

Then modify the `sub_cluster.pbs` file (change parameters like input and output file names)

Finally, submit the job using:

Note: no additional requirements than step 3

```bash
qsub sub_cluster.pbs
```

## Details

Example code in `sub_cluster.pbs`

This cluster sequences at 50% sequence identity

```bash
mmseqs easy-cluster clus2_NR.fasta clus2_NR_s50 tmp/ --min-seq-id 0.5 --threads 96
```

No additional software requirement compared to Step 3.

