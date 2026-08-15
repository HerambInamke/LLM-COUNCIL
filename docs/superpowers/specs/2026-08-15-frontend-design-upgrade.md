# Frontend Design Upgrade: "The Analyst"

## Overview
A structural and aesthetic upgrade to the LLM Council frontend, shifting the UI from a generic chat application to a professional, high-end analytical instrument. The design focuses on legibility, clean structural boundaries, and minimalist typography.

## Palette & Typography
- **Backgrounds**: App background `#FAFAFA`, Card background `#FFFFFF`.
- **Text**: Primary `#1A1A1A`, Secondary `#666666`.
- **Borders & Shadows**: Borders `#E5E7EB` (1px solid), Shadows `0 1px 3px rgba(0,0,0,0.05)`.
- **Accents**: Primary interactive `#2563EB` (Cobalt Blue).
- **Stage 3 (Synthesis)**: Background `#ECFDF5` (Mint), Border/Accent `#059669` (Emerald).
- **Typography**: System font stack (`system-ui, -apple-system, sans-serif`). Clean, readable line heights (`1.6` for markdown body).

## Layout Structure
- **Container**: Max-width centered layout (e.g., `800px` - `900px`) so the text doesn't stretch too wide, improving readability.
- **Message Flow**: Vertical flow. User queries act as large, distinct section headers rather than chat bubbles.
- **Input Area**: A floating, centered "command bar" at the bottom of the screen with a subtle blur/translucent background behind it, rather than a full-width blocky footer.

## Component Details

### `ChatInterface`
- Floating input container at the bottom.
- Clean input field with no heavy borders unless focused.
- Shift+Enter to send, crisp submit icon/button.

### `Stage 1` (Parallel Responses)
- Housed inside a white card with a subtle border and shadow.
- Tab navigation uses a modern "underline" indicator for the active tab (using the `#2563EB` accent) rather than heavy pill backgrounds.
- Markdown content is padded generously (e.g., `24px`).

### `Stage 2` (Peer Review & Ranking)
- Similar card container to Stage 1.
- **Signature Element**: De-anonymized model names in the text and rankings are styled as "badges" (small rounded pills with a light blue background `#EFF6FF` and dark blue text `#1D4ED8`). This replaces the current basic bolding, making the transition from anonymous to known models highly legible and professional.
- Extracted Rankings are presented in clean, numbered list formats with minimal visual noise.

### `Stage 3` (Chairman Synthesis)
- The ultimate conclusion of the request.
- Uses the success palette (Mint/Emerald) to distinctly separate it from the deliberation stages.
- Slightly larger base font size to emphasize it as the final answer.

## Implementation Notes
- All styles will be updated in existing CSS files (`App.css`, `index.css`, component CSS).
- React components will be modified to add the necessary wrapper `div`s for the card styles and badges.
- Custom logic will be added to `Stage2.jsx` to parse model names and wrap them in a `<span className="model-badge">` instead of just `**model**`.
