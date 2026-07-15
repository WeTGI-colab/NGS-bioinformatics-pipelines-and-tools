# WGLS Bioinformatics — pipelines & tools

Interactive overview of the WGLS NGS bioinformatics ecosystem: the two automated clinical pipelines and the standalone tools. Each program shows its **version**, its **input files**, **who runs it**, and a plain-language **explanation on hover**. Tool names link to their repo and reference files link to `WRGLpipeline-files`.

## View it

Once GitHub Pages is enabled, the diagram is live at:

**https://wetgi-colab.github.io/NGS-bioinformatics-pipelines-and-tools/**

(Open `index.html` locally to preview before publishing.)

## What's inside (3 tabs)

- **AmpliconPipeline** — Genotyping · RACP1 · SSrep · PGX (*in validation, not yet in production*). Bash + SLURM + Apptainer, one job per sample. Run by *auto (the server)*.
- **nf_panel** — Nextflow (fork of nf-core/sarek): SNV (HaplotypeCaller), CNV (ExomeDepth), SV (Manta), QC, and Congenica interpretation. Run by *auto (the server)*.
- **Standalone tools** — ClinVar submission (`congenica2clinvar` → `clinvar-upload`, run manually), `panhaem-cov`, `MLPA_facilitator_API`, `SpliceAI-lookup_Docker`, `netcopy`, `sysad`, `QM_trends_tool`, and the **sysad toolkit** (interactive CLI: interop, samtools, bcftools, bedtools, tabix, bgzip, gatk).

## How to read the diagram

- Programs run down the centre; **input files enter from the side** at the exact step where they are used.
- **Hover** any box or file for a short, plain-language explanation.
- 🐳 marks programs that run from a **Docker** image; `NF` marks the Nextflow pipeline.
- Files with a **red border** are **shared between both pipelines** — changing one (e.g. a BED or the reference genome) affects both. Click any file to highlight every step that uses it (within the active tab).
- **Links:** a tool's name links to its repo; reference/BED files link to their file in `WRGLpipeline-files`. These repos are private, so the links only open for members of the `cas-wrgl` org.
- Colours mark assay/stream (Genotyping/RACP/SSrep/PGX, or SNV/CNV/SV/QC/interpretation).
- The **"Pending review"** banner means the content has not yet been validated.

## Enabling GitHub Pages

Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `/ (root)` → Save**. The site publishes in ~1 minute.

## Keeping tool versions up to date (automatic)

A GitHub Action (`.github/workflows/update-versions.yml`) reads the **latest release/tag** of each in-house tool repo and writes the version numbers into `index.html`. It runs every Monday and can also be triggered manually from the **Actions** tab. When you cut a new release in a tool repo (e.g. `v1.0.30`), the diagram updates itself.

**One-time setup:**

1. **Fix `tools.json`** — set each `repo` to the exact `owner/name` of the private repo (the current values are guesses from the READMEs). `where: pname` updates the version pill; `where: header` updates the tab-title version; `suffix` keeps trailing text.
2. **Create a read-only token** — a *fine-grained Personal Access Token* (GitHub → Settings → Developer settings → Fine-grained tokens) with **Repository access = the tool repos** and **Repository permissions → Contents: Read-only**. (A GitHub App with the same read scope works too.)
3. **Add it as a secret** — in this repo: **Settings → Secrets and variables → Actions → New repository secret**, name it **`TOOLS_TOKEN`**, paste the token.
4. Run the workflow once from the **Actions** tab to check it works (the log prints `OK <tool> -> <version>` per repo).

The token only needs **read** access and never leaves GitHub. The Action pushes the updated `index.html` using the built-in repo token.

