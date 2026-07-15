# NGS Bioinformatics — pipelines &amp; tools

Interactive overview of the WGLS NGS bioinformatics ecosystem: the two automated clinical pipelines and the standalone tools, showing each program's **version**, its **input files**, and **who runs it**.

## View it

Once GitHub Pages is enabled, the diagram is live at:

**https://wetgi-colab.github.io/NGS-bioinformatics-pipelines-and-tools/**

(Open `index.html` locally to preview before publishing.)

## What's inside (3 tabs)

- **AmpliconPipeline** — Genotyping · RACP1/2 · SSrep. Bash + SLURM + Apptainer, one job per sample. Run by *auto (the server)*.
- **nf_panel** — Nextflow (fork of nf-core/sarek): SNV (HaplotypeCaller), CNV (ExomeDepth), SV (Manta), QC, and Congenica interpretation. Run by *auto (the server)*.
- **Standalone tools** — ClinVar submission (`congenica2clinvar` → `clinvar-upload`), `panhaem-cov`, `MLPA_facilitator_API`, `SpliceAI-lookup_Docker`, `netcopy`, `sysad`.

## How to read the diagram

- Programs run down the centre; **input files enter from the side** at the exact step where they are used.
- 🐳 marks programs that run from a **Docker** image; `NF` marks the Nextflow pipeline.
- Files in **red (⚠)** are **shared between both pipelines** — changing one (e.g. a BED or the reference genome) affects both. Click any file to highlight every step that uses it.
- Colours mark assay/stream (Genotyping/RACP/SSrep, or SNV/CNV/SV/QC/interpretation).

## Enabling GitHub Pages

Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `/ (root)` → Save**. The site publishes in ~1 minute.
