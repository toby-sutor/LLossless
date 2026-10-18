# Build the whitepaper. `make` gives you paper/main.pdf.
#
# The canonical build is containerised TeX Live, pinned by digest. The reason
# is not portability, it is that a paper built against whatever TeX the author
# happened to have installed is a paper nobody else can reproduce, and this one
# argues for reproducibility. A host build is available and is the fast path;
# it is not the one a result is checked against.
#
# Sandbox note: in the VSCodium Flatpak sandbox podman lives on the host, so
# every container command goes through flatpak-spawn. Detected, not configured
# -- the same checkout is used from inside and outside the sandbox.

IMAGE  := docker.io/texlive/texlive@sha256:4984977ccf5afe883cb382d0163f267de0d029d140bb7a9e8f4c19f0b781d57b
# ^ texlive/texlive:latest-full as of 2026-08-30. Pinned by index digest, so
#   `latest-full` moving does not move the paper. Repin deliberately, in a
#   commit that says why.
PODMAN := $(shell test -f /.flatpak-info && echo "flatpak-spawn --host podman" || echo podman)
HOSTDIR := $(shell cd . && pwd)
RECORDS ?= records

# `z` is the SELinux relabel suffix and is required on this host; without it
# the container sees an empty bind mount and latexmk fails on a missing file.
# The web-interface screenshot is the published one in `docs/img/`, not a copy
# that could drift from it, so that directory is mounted read-only where the
# section's `../docs/img/` path lands inside the container.
RUN := $(PODMAN) run --rm -v "$(HOSTDIR):/paper:z" \
       -v "$(HOSTDIR)/../docs/img:/docs/img:ro,z" -w /paper --userns=keep-id $(IMAGE)

LATEXMK := latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

.PHONY: all numbers stamp check paper host clean image
all: paper

# The number generator and the number check are maintained in the working
# repository and are not part of a published copy. Where they are absent the
# targets below say so and build from the committed generated/ files, which
# carry every figure with its record, sha256 and JSON path.
NUMBERS_TOOL := ../internal/paper/figures/build_numbers.py
CHECK_TOOL   := ../internal/paper/check_numbers.py

# Regenerate the figures from the graded records. Not a prerequisite of
# `paper`: records are inputs, and a build that silently rebuilt them would
# hide the day they went missing.
numbers:
	@if [ -f $(NUMBERS_TOOL) ]; then python3 $(NUMBERS_TOOL) --records "$(RECORDS)"; \
	else echo "numbers: the generator is not in this copy; generated/ is used as committed"; fi

# The build stamp is the one generated value that IS a prerequisite of the
# paper, for the opposite reason: it reads .git, which is always present, and a
# stamp left over from the last `make numbers` would name a commit that did not
# build this PDF. It rewrites two lines and touches no measured figure.
stamp:
	@if [ -f $(NUMBERS_TOOL) ]; then python3 $(NUMBERS_TOOL) --stamp; \
	else echo "stamp: the generator is not in this copy; the committed stamp is used"; fi

# The gates. Each runs its own seeded probes first, then the real file.
check:
	@if [ -f $(CHECK_TOOL) ]; then python3 $(CHECK_TOOL); \
	else echo "check: the number check is not in this copy; skipped"; fi
	python3 check_refs.py

paper: stamp check
	$(RUN) $(LATEXMK)

# The fast path, for drafting. Same check, host TeX.
host: stamp check
	$(LATEXMK)

image:
	$(PODMAN) pull $(IMAGE)

clean:
	rm -f main.pdf main.aux main.log main.out main.bbl main.blg main.fls \
	      main.fdb_latexmk main.toc
