# Post-bootstrap independent review

- Review date: 2026-07-30
- Repository: `kooiei-in4a/amane-ai-lab`
- Base branch: `main`
- Base SHA: `c6e6cf982ff5c1772c609701419c2a86ae97b364`
- Review branch: `review/post-bootstrap-hardening`
- Reviewed code head: `0b9be3727b2f7fa8f5d3d1e79d6d89f08c46bdc1`
- Reviewer role: independent architecture / security / reliability reviewer

## Review scope

The review checked the implementation directly against:

- `docs/specs/public-knowledge-base-spec.md`
- `docs/adr/0001-static-site-architecture.md`
- `docs/adr/0002-structured-content-source-of-truth.md`
- `docs/adr/0003-ai-agent-governance.md`
- `docs/agent-prompts/bootstrap-implementation.md`
- `AGENTS.md`

Reviewed implementation areas included source-of-truth boundaries, generated artifacts, HTML sanitization, article generation, content validation, sensitive-data detection, agent entry files, giscus mapping, GitHub Actions, and tests.

## Evidence reviewed before changes

The initial bootstrap validation workflow completed successfully on the bootstrap PR merge candidate:

- Build: 1 article generated
- Content validation: `success=15 warnings=0 errors=0`
- Sensitive-data scan: `scanned_files=79 findings=0`
- Unit tests: 7 passed
- Internal links: 1 article link present

That successful run did not prove the negative cases described below because the original workflow and tests did not exercise them.

## Initial findings

### Blocker

#### SEC-001: Sensitive-data findings echoed the matched source line into CI logs

`check_sensitive_data.py` printed a snippet of the matched line. If a real credential were committed, the scanner could copy that credential into public or broadly accessible Actions logs, creating a second disclosure channel.

A line containing any `[REDACTED_*]` marker was also skipped entirely, so a real secret and a redaction marker on the same line bypassed detection.

### Major

#### GEN-001: Generated article output was not synchronized with the source of truth

`build_site.py` overwrote expected pages but did not remove output directories whose source article had been removed or renamed. A stale generated page could therefore remain in `articles/` and in a Pages artifact after its authoritative source disappeared.

#### CI-001: Generated-drift detection ignored untracked generated files

The validation workflow used `git diff --quiet`. Git does not include untracked files in that check, so a newly generated article page omitted from a commit could pass the drift gate.

The workflow also ran generation only once and did not establish idempotency.

#### PAGES-001: Pages artifact assembly was not gated by the repository validation suite

The Pages artifact workflow built and uploaded an artifact without running content validation, sensitive-data detection, or unit tests. It also granted `pages: write` and `id-token: write` even though it did not deploy.

### Minor

#### SEC-002: Safe email-domain matching accepted suffix lookalikes

An address at `notexample.com` was treated as safe because the implementation used a simple string suffix check for `example.com`.

#### TEST-001: Negative regression coverage was insufficient

The original tests did not cover Markdown script sanitization, stale generated pages, redaction-marker bypass, exact safe-domain matching, or high-risk `.env` file recognition.

## Fixes applied

- Removed matched secret values from scanner return/log output.
- Removed redaction placeholders before matching instead of skipping the whole line.
- Changed safe email handling to exact domain comparison.
- Added high-risk text-file recognition for `.env*`, `Dockerfile`, and common configuration suffixes.
- Made article generation pre-render all valid sources, then recreate the generated `articles/` tree before writing pages.
- Added validation for stale generated article directories.
- Replaced `git diff --quiet` drift checks with `git status --porcelain --untracked-files=all` over all generated paths.
- Added a second generation pass and a second clean-tree check.
- Gated Pages artifact assembly on build idempotency, content validation, sensitive-data detection, and unit tests.
- Reduced the Pages artifact workflow permission to `contents: read`.
- Added regression tests for the corrected failure modes.

## Post-fix validation

Validation workflow run `30544167172` completed successfully against code head `0b9be3727b2f7fa8f5d3d1e79d6d89f08c46bdc1`.

Executed gates:

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py
git status --porcelain=v1 --untracked-files=all -- articles data index.html sitemap.xml feed.xml
python scripts/build_site.py
git status --porcelain=v1 --untracked-files=all -- articles data index.html sitemap.xml feed.xml
python scripts/validate_content.py
python scripts/check_sensitive_data.py
python -m unittest discover -s tests -v
```

Results:

- First build: 1 article generated; generated-tree status clean.
- Second build: 1 article generated; generated-tree status remained clean and idempotent.
- Content validation: `success=15 warnings=0 errors=0`.
- Sensitive-data scan: `scanned_files=80 findings=0`.
- Unit tests: 12 passed.
- Internal links: 1 article link present.

An earlier review-branch run correctly failed because a negative-test fixture committed a secret-like assignment literally. The fixture was changed to construct the value only at test runtime, retaining the negative test without weakening repository-wide scanning.

## Remaining findings

### Blocker

None.

### Major

None.

### Minor

- `new_article.py` derives the next ID from currently present articles. Deleting the highest allocated article could permit that ID to be reused. An append-only ID registry or an explicitly approved history-based rule should be decided before article deletion is supported routinely.
- GitHub Actions dependencies use major-version tags rather than immutable commit SHAs. Pinning can be considered as a later supply-chain hardening change.

### Suggestion

- Decide explicitly whether `draft` and `review` articles should be included in the public Pages artifact. The public repository already exposes source files, but the website publication semantics are not explicit enough to change in this hardening review.

## Human work still required

- Configure GitHub Pages deployment separately after validation of the artifact workflow.
- Enable GitHub Discussions and configure the real giscus repository/category IDs.
- Review and merge the Draft PR; the agent must not merge or publish.

## Final decision

`PASS WITH MINOR FINDINGS`.

All Blocker and Major findings identified in this review were resolved with limited changes, and the strengthened validation workflow completed successfully with clean two-pass generation.
