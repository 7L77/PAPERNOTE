---
name: paper-reader
description: |
  Use when the user asks to read, analyze, summarize, or critique an academic paper,
  or when they provide a paper PDF / arXiv link / Zotero item. Trigger on phrases such as
  "read paper", "analyze paper", "summarize paper", "读论文", "分析文献", "帮我读",
  "读一下这篇", "论文笔记". Specialized for CV/DL papers but usable for other ML papers.

  Also use when the user asks to extract a paper's method into traceable pseudocode or
  a method note, including phrases such as "提取论文方法", "方法伪代码", "伪代码",
  "整理方法到 NAS方法", "extract method", "extract pseudocode".

  Important trigger: if the user says "读一下 XXX", "读一下这篇", or "帮我读",
  this skill must be used.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Paper Reader

Read papers, generate structured notes, maintain concept notes, archive source PDFs, archive paper code when available, and generate traceable method notes. For concept and method outputs, also generate paired Chinese versions.

Start every run with a short acknowledgement to the user.

## Hard rule for normal "read paper" requests

If the user says `读一下`, `帮我读`, `读论文`, `analyze paper`, or otherwise asks to read a paper without explicitly requesting `quick` / `快速看` / `快速总结`, treat it as a **full run**.

A full run must not stop at a chat reply. It must produce the on-disk outputs required by this skill in the same run:

1. archive the PDF
2. archive official code when available
3. generate or update the structured paper note
4. generate or update the method note
5. maintain missing concept notes
6. refresh indexes when enabled

Do not satisfy a normal read request with only a prose summary in the chat response.
If any required artifact is intentionally skipped, state exactly what was skipped and why.

## Step 0: Load shared config

Read `../_shared/user-config.json` first. If `../_shared/user-config.local.json` exists, let it override the shared config.

Derive and reuse these variables:

- `VAULT_PATH`
- `NOTES_PATH = {VAULT_PATH}/{paper_notes_folder}`
- `CONCEPTS_PATH = {NOTES_PATH}/{concepts_folder}`
- `ZOTERO_DB`
- `ZOTERO_STORAGE`
- `AUTO_REFRESH_INDEXES`
- `GIT_COMMIT_ENABLED`
- `GIT_PUSH_ENABLED`

### Local path overrides for this vault

If these folders exist, they override config-derived paths:

- Concept notes: `D:/Project/paper/论文笔记/_概念`
- Method notes: `D:/Project/paper/论文笔记/NAS方法`
- Code depots: `D:/Project/paper/code_depots`

When present, use these exact on-disk paths even if the config contains a differently encoded folder name.

## 1. Accepting the paper

Supported inputs:

- PDF path: read directly
- arXiv link: prefer `https://arxiv.org/html/{arxiv_id}` when available
- Zotero collection or search query
- DOI / title search when PDF is missing

When no local PDF is available, fetch in this order:

1. arXiv HTML
2. arXiv PDF
3. DOI landing page
4. Web search by paper title

For Zotero details, read `references/zotero-guide.md` only when needed.

## 1.5 Paper PDF archiving is mandatory

For every normal paper-read run, archive the paper PDF locally.

Canonical archive folder:

- `D:/Project/paper/papers`

Rules:

1. Create the folder if it does not exist.
2. Download or copy the source PDF into that folder.
3. Name the file with the paper title as the stem and `.pdf` as the extension.
4. Sanitize Windows-invalid filename characters such as `<>:"/\\|?*` and trim trailing dots/spaces.
5. Before downloading, deduplicate by normalized title stem:
   case-insensitive, ignore extra spaces, and treat `_` / `-` / space variants as equivalent.
6. If an equivalent archived PDF already exists, skip the download.
7. Prefer true PDF content. Do not save an HTML page with a `.pdf` extension.

Record the final archived PDF path in the paper note when practical.

## 1.6 Paper code archiving is mandatory when code exists

For every normal paper-read run, if the paper has an official code repository or clearly referenced implementation, archive it locally.

Canonical code archive folder:

- `D:/Project/paper/code_depots`

Rules:

1. Create the folder if it does not exist.
2. Prefer official code links from the paper, arXiv page, project page, or the paper note metadata.
3. Use a subdirectory named with the paper title:
   `D:/Project/paper/code_depots/{PaperTitle}`
4. Sanitize Windows-invalid path characters such as `<>:"/\\|?*` and trim trailing dots/spaces.
5. Before downloading, deduplicate by normalized title directory name:
   case-insensitive, ignore extra spaces, and treat `_` / `-` / space variants as equivalent.
6. If an equivalent code directory already exists, skip the download.
7. For GitHub / git repositories, prefer `git clone` into the title directory.
8. If cloning is not possible but a downloadable source archive exists, save and extract it into the title directory.
9. Do not clone unrelated third-party repos just because they are mentioned in baselines; archive only the code corresponding to the target paper unless the user explicitly asks otherwise.

Record the final local code path in the paper note and method note when practical.

### Code-first rule for method extraction

When the target paper has official code:

1. Archive the code first.
2. Inspect the local codebase before finalizing the method note.
3. Use the code to sharpen implementation details, module boundaries, training/inference flow, and practical notes.
4. Keep the paper as the primary source for claims, equations, and algorithm intent; use the code as implementation evidence.

When the target paper has no code:

1. Do not block on code search forever.
2. Finalize the method note directly from the paper.
3. Mark implementation details as paper-derived when they cannot be verified in code.

## 2. Modes

Choose the smallest mode that satisfies the request.

| Mode | Triggers | Output |
|---|---|---|
| Quick summary | `quick`, `快速看`, `快速总结` | 3-5 sentence summary |
| Full analysis | default, `详细分析`, `论文笔记`, plain `读一下`, plain `帮我读` | structured paper note + method note + concept maintenance |
| Critique | `critique`, `批判性分析` | strengths, risks, assumptions |
| Formula / technical extraction | `提取公式`, `技术细节` | equations, algorithm details |
| Method extraction | `提取论文方法`, `方法伪代码`, `整理方法到 NAS方法` | separate method note in `NAS方法/` |

## 3. Paper note generation

Use `assets/paper-note-template.md`.

Non-negotiable quality rules:

1. Include all important figures, formulas, and tables from the paper note-worthy content.
2. Use `[[Concept]]` links for technical terms on first mention when they deserve a concept note.
3. Explain formulas with meaning and symbols, not just raw LaTeX.
4. Prefer external image links from arXiv HTML / project page / GitHub. Fall back to local extraction only if needed.
5. Keep the note traceable to sections, figures, tables, equations, and algorithms in the source paper.

For detailed figure / formula / table standards, read `references/quality-standards.md` only when needed.
For image fallback details, read `references/image-troubleshooting.md` only when needed.

## 4. Saving the paper note

Default note filename:

- `{MethodName}.md`

Default paper note path:

- `{NOTES_PATH}/{zotero_collection_path}/{MethodName}.md`
- If no Zotero path is known, save directly under `{NOTES_PATH}`

Required frontmatter fields:

```yaml
---
title: "Paper Title"
method_name: "MethodName"
authors: [Author1, Author2]
year: 2025
venue: arXiv
tags: [tag1, tag2]
zotero_collection: ""
image_source: online
arxiv_html: https://arxiv.org/html/xxxx
created: YYYY-MM-DD
---
```

Add local paths when they are available:

- `local_pdf: D:/Project/paper/papers/{PaperTitle}.pdf`
- `local_code: D:/Project/paper/code_depots/{PaperTitle}`

## 5. Concept maintenance is mandatory

After generating or updating the paper note, always maintain concept notes under the canonical concept folder.

Canonical concept folder:

- Prefer `D:/Project/paper/论文笔记/_概念` if it exists
- Otherwise use `{CONCEPTS_PATH}`

Workflow:

1. Scan the paper note for all `[[Concept]]` links.
2. Add any missing high-value concepts that clearly deserve notes even if they were not linked initially.
3. Deduplicate before creating any concept note.
4. Reuse existing concept notes when duplicates are found.
5. Create only truly missing concept notes.

### Concept deduplication rules

Apply these checks in order:

1. Exact file stem match.
2. Case-insensitive normalized match after removing spaces, hyphens, and underscores.
3. Singular/plural and acronym/full-name matches when the equivalence is obvious from the paper.
4. Frontmatter alias match or first-heading match.

When a duplicate is found:

- Skip creating a new file.
- Reuse the existing note.
- If useful, append the current paper under `代表工作` or an equivalent section.

When a concept is missing:

- Create the note directly under `D:/Project/paper/论文笔记/_概念` when that folder exists.
- Otherwise create it under `{CONCEPTS_PATH}`.
- Use `assets/concept-note-template.md` for the English note, `assets/concept-note-template-ch.md` for the Chinese note, and `references/concept-categories.md` for category guidance.
- Also create a Chinese companion note in the same folder, with the same English stem plus `_ch`.
  Example: `Spatial Encoding.md` and `Spatial Encoding_ch.md`.

Minimum concept note contents:

- plain-language intuition
- why the concept matters
- one tiny example / toy scenario / analogy when the concept is abstract
- precise definition
- key points
- representative papers
- related concepts

Concept-note writing rules:

1. Write for a technically literate reader who has not seen the term before.
2. Lead with intuition first. Do not start with notation unless the concept is inherently mathematical.
3. Include at least one concrete example, toy case, or analogy when the concept is easy to misunderstand.
4. If you include formulas, explain every symbol in plain language and say what the formula is doing.
5. When the concept appears in the current paper, add one short note about how that paper uses it.
6. Avoid circular definitions and jargon loops such as "X is a framework for doing X-like optimization."

### Chinese concept companion rule

For every English concept note that is created or updated:

1. Create or update a Chinese companion note in the same folder.
2. Filename rule: `{EnglishStem}_ch.md`
3. Keep the English method / concept identifier in the title or first paragraph so cross-reference remains obvious.
4. The Chinese note should not be a machine-translated word salad. Keep it concise, readable, and aligned with the English source note.
5. If the `_ch` file already exists, update it instead of creating a duplicate.

## 6. Method extraction is a default output for normal reads

This is a separate output from the paper note and should be produced by default for normal paper-read requests, not only on explicit request.

Output path:

- Prefer `D:/Project/paper/论文笔记/NAS方法/{MethodName}.md` if the folder exists
- Otherwise create `{NOTES_PATH}/NAS方法/{MethodName}.md`

Deduplication:

1. If a file with the same method name already exists, update it instead of creating a duplicate.
2. If a clearly equivalent method note exists under another normalized spelling, update that file.

Use `assets/nas-method-template.md`.
Also create a Chinese companion file using `assets/nas-method-template-ch.md`.

Every method note must include:

1. Method name and source paper metadata.
2. One-paragraph method summary.
3. Applicable scenarios:
   problem type, assumptions, data regime, constraints, and scale where the method fits.
4. Non-applicable or risky scenarios.
5. Inputs, outputs, objective, and core assumptions.
6. Traceable pseudocode:
   every major block must cite the paper source, such as section number, figure number, algorithm number, or equation number.
7. Training pipeline and inference pipeline when both exist.
8. Complexity / efficiency / runtime characteristics when the paper provides them.
9. Implementation notes:
   hyperparameters, masking, optimization tricks, required modules, and practical gotchas.
10. Comparison to baselines or predecessor methods.
11. References:
   arXiv link, HTML link, code link, and citation targets.
12. Local implementation path when code is archived.

Method-note source priority:

1. If official code exists, archive and inspect the code before completing the method note.
2. Then reconcile code structure with the paper's sections, equations, figures, and algorithms.
3. If paper and code differ, say so explicitly in the note.
4. If no code exists, state that the method note is paper-only and continue.

### Chinese method companion rule

For every English method note that is created or updated:

1. Create or update a Chinese companion note in the same folder.
2. Filename rule: `{MethodName}_ch.md`
3. Keep the pseudocode traceability markers intact, including `Source: Sec. X / Eq. Y / Alg. Z`.
4. Translate the explanations, scenarios, and implementation notes into Chinese, but keep paper-specific identifiers, equations, and method names stable.
5. If the `_ch` file already exists, update it instead of creating a duplicate.

### House style for NAS method notes

- Treat `D:/Project/paper/论文笔记/NAS方法/DeCoST.md` as the canonical house-style reference when that file exists.
- Preserve the section order used there unless the paper truly lacks the corresponding content.
- Keep the note practical: say when the method fits, when it fails, what assumptions it needs, and what code-level details matter.
- Avoid vague headings filled with generic claims. If the paper does not report a detail, say `Not reported in the paper` instead of inventing filler.

### Traceability rules for pseudocode

- Do not write pseudocode with no provenance.
- Add `Source: Sec. X`, `Source: Alg. Y`, `Source: Eq. (Z)`, or similar after each major block.
- If a step is not stated directly in the paper and you infer it, mark it explicitly as `Inference from source`.
- Keep the pseudocode faithful to the paper's named method, not to a generic implementation you prefer.

## 7. Default behavior after a normal paper-read request

Unless the user explicitly asks for only a quick summary:

1. Read the paper.
2. Archive the PDF into `D:/Project/paper/papers` using the paper title as the filename and skip duplicates.
3. Archive the official code into `D:/Project/paper/code_depots/{PaperTitle}` when code exists, and skip duplicates.
4. Generate or update the structured paper note.
5. Maintain concept notes with deduplication.
6. If code exists, inspect the archived code before finalizing the separate method note in `NAS方法/`.
7. If no code exists, finalize the method note directly from the paper.
8. For all generated concept notes and method notes, also generate or update the paired Chinese `_ch` files.
9. Refresh indexes if enabled.

Completion rule:

- Do not stop after step 1, 2, or a chat-only summary.
- A normal read request is complete only after the note files and concept updates are written to disk, unless a concrete blocker is stated.

## 8. Post-save automation

If `AUTO_REFRESH_INDEXES=true`, run:

```bash
python3 ../_shared/generate_concept_mocs.py
python3 ../_shared/generate_paper_mocs.py
```

If `GIT_COMMIT_ENABLED=true` and `{VAULT_PATH}/.git` exists, stage the created note files and commit them.
Only push when `GIT_PUSH_ENABLED=true`.

## 9. Batch processing

Batch mode is supported for Zotero collections:

1. enumerate papers
2. deduplicate
3. skip already processed notes
4. process each paper
5. summarize the results

## References to load only when needed

- `references/zotero-guide.md`
- `references/image-troubleshooting.md`
- `references/concept-categories.md`
- `references/quality-standards.md`
