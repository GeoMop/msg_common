# Project instructions

*Write project specific instructions here*

# Generic instructions
Follow unless repository specific instruction dosn't explicitly say otherwise.

## 1. Repository workflow

- Start from `main.tex`. Treat it as the entry point, preamble, macro registry,
  bibliography setup, glossary source, and document assembly file.
- Use `build.sh` for compilation. Prefer the repository workflow over ad hoc
  LaTeX commands.
- Run the build yourself before completing source edits.
- Do not commit changes.
- Treat comments containing `AGENT` as local context instructions for the
  surrounding source.
- Preserve comments containing `AGENT`. Keep the original comment and, if
  useful, append at most one short line describing how it was resolved.
- Keep edited source lines near 90 characters where practical.
- If a build fails, try to fix the source or build setup before stopping.
- Run read-only output inspection only when requested or when debugging a build
  or formatting issue.
- For PDF inspection, prefer CLI tools such as `pdftotext` or `pdfinfo`.
- Ask the user to inspect output only after you have completed your own checks.

## 2. Shared scientific-writing rules

### 2.1 Style

- Prefer precise, neutral, evidence-based prose.
- Write densely, but define symbols, assumptions, and technical terms when first
  needed.
- Keep conclusions traceable to results, figures, tables, or cited sources.
- Avoid promotional language, vague claims, and unsupported interpretation.

### 2.2 Math and notation

- Use `$...$` for inline math and `\[...\]` for display math.
- Reuse macros defined in `main.tex`; do not reintroduce raw notation when an
  existing macro covers it.
- Keep notation consistent across the whole document.
- Use project macros for vectors, tensors, operators, norms, and units, e.g.
  `\vc{}`, `\tn{}`, `\grad`, `\div`, `\norm{}`, `\abs{}`.

### 2.3 Terminology and acronyms

- Preserve established terminology within the manuscript.
- If a glossary is present, keep using it until final cleanup.
- Reuse existing acronyms; avoid introducing new ones unless the document
  clearly requires them.
- On first use in new text, follow the document’s glossary or acronym style
  rather than hardcoding abbreviations.
- Do not alternate between equivalent spellings inside one local context.

### 2.4 References, figures, and tables

- Preserve and extend cross-references; never replace them with hardcoded
  numbers.
- Match the local source style for figures, tables, sections, chapters, and
  equations.
- Label any new section, float, or equation that may be referenced later. Use
  `fig`, `sec`, and `tab` prefixes; equation labels stay without a prefix.
- This rule applies only to newly introduced labels. Do not rename existing
  user-defined labels.
- Captions should make figures and tables understandable on their own, while
  interpretation and detail stay in the main text.
- If the source already states that a figure or table is adapted or reused,
  preserve that attribution.

## 3. Article-specific rules

- Optimize for one clear research question or technical claim.
- Keep only material that supports the paper argument; move broad background to
  short context paragraphs or appendices.
- Prefer a tight structure: introduction, method/model, results, discussion,
  conclusion.
- When shortening text, keep assumptions, parameter definitions, and evaluation
  criteria explicit.
- Figures and tables should carry argumentative weight, not serve as general
  archive material.

## 4. Technical-report-specific rules

- Optimize for traceability, reproducibility, and practical use.
- State scope, inputs, assumptions, methods, outputs, and limitations
  explicitly.
- Prefer complete procedural descriptions over article-style compression when
  the information is needed for reuse or review.
- Keep recommendations tied to observed data, calculations, or stated criteria.
- Use appendices for supporting detail that would interrupt the main flow but
  should remain available to the reader.

## 5. Resolving doubts and inconsistencies

- Keep a final section in `PLAN.md` or a similar planning file for unresolved
  manuscript inconsistencies, open questions, and suggestions that go beyond
  the existing text. Create `PLAN.md` if no planning file exists.
- If local macros or reference commands conflict with these rules, follow the
  source and note the conflict in the planning file.
- If document-specific instructions are missing, infer the document type from
  `main.tex` and state the assumption.
- Use glossary or acronym machinery only if the project already provides it.

## 6. Build configuration

- Use `build.sh` for normal local compilation.
- `build.sh` builds `main.pdf` and, when a Git reference is available, also
  builds `main-d.pdf` as a comparison PDF.
- Use `latexmkrc` for hosted editors such as Overleaf and for direct `latexmk`
  use.
- If a project needs special latexdiff handling for macros, define it in
  `latexmkrc`.
- On Overleaf, a plain build should work without local Git state. If
  `main-old.tex` is present, `latexmkrc` may also build a diff PDF.
