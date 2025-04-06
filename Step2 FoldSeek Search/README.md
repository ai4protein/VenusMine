# Step 2: FoldSeek Search

There are 2 stages in this step:
- Run FoldSeek search in [FoldSeek webserver](https://search.foldseek.com/search)
  - Use the prepared start points in step 1
  - Download the **hit table** `.m8` files
- Run local jupyter notebook `foldseek_result_analysis.ipynb`
  - Some file name / folder name should be adjusted
  - Save a `{folder_name}_foldseek.fasta` file in the correspond foldseek result folder
  - Running this code does not need other installed packages


The file tree should be:
```
Step2 FoldSeek Search/
├── xxx(protein_name)/
│   ├── alis_afdb-proteome.m8
│   ├── alis_afdb-swissprot.m8
│   ├── alis_afdb50.m8
│   ├── alis_cath50.m8
│   ├── alis_gmgcl_id.m8
│   ├── alis_mgnify_esm30.m8
│   ├── alis_pdb100.m8
└── foldseek_result_analysis.ipynb
``​`

Some bugs might because:
- Chinese names or spaces in file name




