# Atlas v2 prototype — Design QA

- Source visual truth: `design/atlas-v2-master-target.png`
- Source pixels: 1536 × 1024
- Intended implementation viewport: 1440 × 1024 CSS px, device scale 1
- State: História, 1969, Porsche 917, modal fechado
- Browser target: Chrome desktop
- Build result: passed
- Sites worker tests: 4/4 passed
- Dependency refresh: React 19.2.8, React DOM 19.2.8, Vite 8.2.2,
  `@vitejs/plugin-react` 6.1.0
- Production dependency audit: 0 vulnerabilities

## Evidence status

The source visual is available locally and the implementation builds. A
browser-rendered implementation screenshot could not be captured. The Chrome
validation was retried after the first GitHub checkpoint, but the connected
browser runtime still references the removed plugin build `26.818.21641`
instead of the installed `26.818.22352` build.

Without the implementation screenshot there is no valid full-view or focused
region comparison. Build output and source inspection are not substitutes for
visual evidence.

## Findings

- [P0] Browser-rendered comparison is missing.
  - Location: complete 1440 × 1024 primary screen.
  - Evidence: source image exists; equivalent implementation capture does not.
  - Impact: typography, crop, spacing, controls and responsive fidelity cannot
    be approved.
  - Fix: reconnect Chrome or repair the in-app browser runtime, capture the
    1969 state at 1440 × 1024, test primary interactions, and compare the two
    images in one visual input.

## Interaction checks pending

- Timeline range and milestone selection.
- História and Mapa/Globo switching.
- Six discovery journeys.
- Immersive chapter modal open/close.
- Keyboard left/right and Escape.
- Browser console errors.

## Comparison history

- Initial pass: blocked before comparison because browser evidence was not
  available. No visual fixes are claimed from this pass.
- Retry after dependency refresh: Chrome remained blocked by the stale browser
  runtime reference. The production build and four hosting tests passed again,
  but they are not substituted for visual evidence.

## Follow-up polish

None classified until the blocking comparison is completed.

final result: blocked
