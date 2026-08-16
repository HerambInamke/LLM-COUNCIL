# Frontend Design Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the frontend design to "The Analyst" aesthetic (clean, minimalist, highly legible cards, badge elements, and a floating command bar).

**Architecture:** We will implement the design defined in the spec by updating global CSS variables and layouts, reshaping the `ChatInterface` into a floating bottom bar, applying "card" styles to the stages to break up text walls, and intercepting markdown rendering in `Stage2` to render beautiful inline model badges.

**Tech Stack:** React, plain CSS, ReactMarkdown.

**Spec:** `docs/superpowers/specs/2026-08-15-frontend-design-upgrade.md`

## Global Constraints
- Maximum content width should be constrained (e.g., `900px`) for readability.
- The app background is `#FAFAFA` and cards are `#FFFFFF`.
- Use the system font stack (`system-ui, -apple-system, sans-serif`).
- Accent color for interactive elements is `#2563EB`.

---

### Task 1: Global Styles & Layout

**Files:**
- Modify: `frontend/src/index.css`
- Modify: `frontend/src/App.css`

**Interfaces:**
- Consumes: N/A
- Produces: CSS variables (e.g. `--bg-app`, `--bg-card`, `--accent`) and constrained `.app` layout that subsequent tasks will use.

- [ ] **Step 1: Define CSS Variables and global typography in `index.css`**
Update `:root` in `frontend/src/index.css` to define the palette:
```css
:root {
  --bg-app: #FAFAFA;
  --bg-card: #FFFFFF;
  --text-primary: #1A1A1A;
  --text-secondary: #666666;
  --accent: #2563EB;
  --border-color: #E5E7EB;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
  
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  color: var(--text-primary);
  line-height: 1.6;
}
body { background: var(--bg-app); margin: 0; }
.markdown-content { padding: 0; } /* Remove the old 12px padding, we handle it in cards */
.markdown-content p { color: var(--text-primary); }
```

- [ ] **Step 2: Constrain layout in `App.css`**
Update `frontend/src/App.css`. Center the main content area so lines don't get too long.
```css
.app {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: var(--bg-app);
  justify-content: center; /* Center the layout */
}

/* Assume the main content area has a class like .main-content */
.main-content {
  flex: 1;
  max-width: 900px;
  width: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 24px 120px 24px; /* padding-bottom to avoid overlap with floating input */
  display: flex;
  flex-direction: column;
  gap: 24px;
}
```

- [ ] **Step 3: Modify `App.jsx` to apply layout classes**
If `App.jsx` doesn't use `.main-content` and `.messages`, update its return statement to wrap the conversation history appropriately. Ensure the `ChatInterface` and `.messages` list sit inside the `max-width` container.

- [ ] **Step 4: Commit**
```bash
git add frontend/src/index.css frontend/src/App.css frontend/src/App.jsx
git commit -m "style: apply global analyst theme and layout"
```

---

### Task 2: Floating Command Bar Input

**Files:**
- Modify: `frontend/src/components/ChatInterface.css`

**Interfaces:**
- Consumes: CSS variables from Task 1.
- Produces: A floating input area fixed to the bottom of the `.main-content` container.

- [ ] **Step 1: Update `ChatInterface.css`**
Replace the blocky styling with a floating, translucent look.
```css
.chat-interface {
  position: absolute;
  bottom: 24px;
  left: 24px;
  right: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  padding: 12px;
  z-index: 10;
}

.chat-interface textarea {
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  font-family: inherit;
  font-size: 1rem;
  color: var(--text-primary);
  padding: 8px;
}

.chat-interface button {
  align-self: flex-end;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.chat-interface button:hover:not(:disabled) {
  opacity: 0.9;
}

.chat-interface button:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}
```

- [ ] **Step 2: Commit**
```bash
git add frontend/src/components/ChatInterface.css
git commit -m "style: implement floating command bar for chat interface"
```

---

### Task 3: Stage 1 Card Layout & Clean Tabs

**Files:**
- Modify: `frontend/src/components/Stage1.css`

**Interfaces:**
- Consumes: `.stage` wrapper div in `Stage1.jsx`.

- [ ] **Step 1: Update `Stage1.css`**
Turn the stage into a white card with an underline tab system.
```css
.stage {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  padding: 24px;
  margin-bottom: 24px;
}

.stage-title {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.tabs {
  display: flex;
  gap: 16px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 20px;
}

.tab {
  background: transparent;
  border: none;
  padding: 8px 4px;
  cursor: pointer;
  color: var(--text-secondary);
  font-weight: 500;
  position: relative;
}

.tab.active {
  color: var(--accent);
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent);
}

.tab-content {
  padding: 0 4px;
}
```

- [ ] **Step 2: Commit**
```bash
git add frontend/src/components/Stage1.css
git commit -m "style: apply card layout and modern tabs to Stage 1"
```

---

### Task 4: Stage 2 Model Badges & Typography

**Files:**
- Modify: `frontend/src/components/Stage2.jsx`
- Modify: `frontend/src/components/Stage2.css`

**Interfaces:**
- Consumes: Card styles from `Stage1.css` (they share `.stage`).
- Produces: Custom `ReactMarkdown` rendering for `<strong/>` tags to generate badges.

- [ ] **Step 1: Update `deAnonymizeText` in `Stage2.jsx`**
Instead of `**modelShortName**`, use `**MODEL:modelShortName**` so we can intercept it safely.
```javascript
// In Stage2.jsx
function deAnonymizeText(text, labelToModel) {
  if (!labelToModel) return text;
  let result = text;
  Object.entries(labelToModel).forEach(([label, model]) => {
    const modelShortName = model.split('/')[1] || model;
    result = result.replace(new RegExp(label, 'g'), `**MODEL:${modelShortName}**`);
  });
  return result;
}
```

- [ ] **Step 2: Update `<ReactMarkdown>` in `Stage2.jsx`**
Provide a custom `components` object to intercept the bold text.
```javascript
<ReactMarkdown
  components={{
    strong: ({node, children, ...props}) => {
      const text = String(children);
      if (text.startsWith('MODEL:')) {
        return <span className="model-badge">{text.replace('MODEL:', '')}</span>;
      }
      return <strong {...props}>{children}</strong>;
    }
  }}
>
  {deAnonymizeText(rankings[activeTab].ranking, labelToModel)}
</ReactMarkdown>
```

- [ ] **Step 3: Style the badges and rankings in `Stage2.css`**
```css
.model-badge {
  display: inline-block;
  background: #EFF6FF;
  color: #1D4ED8;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.85em;
  font-weight: 600;
  margin: 0 4px;
  border: 1px solid #BFDBFE;
}

.parsed-ranking {
  margin-top: 24px;
  padding: 16px;
  background: #F9FAFB;
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.aggregate-rankings {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
}

.aggregate-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #F3F4F6;
}

.aggregate-item:last-child {
  border-bottom: none;
}

.rank-position {
  font-weight: bold;
  color: var(--text-secondary);
  width: 24px;
}
```

- [ ] **Step 4: Commit**
```bash
git add frontend/src/components/Stage2.jsx frontend/src/components/Stage2.css
git commit -m "feat: add model badges and refine Stage 2 layout"
```

---

### Task 5: Stage 3 Chairman Synthesis (Success Styling)

**Files:**
- Modify: `frontend/src/components/Stage3.css`

**Interfaces:**
- Consumes: N/A

- [ ] **Step 1: Update `Stage3.css`**
Apply the distinct Mint/Emerald palette to distinguish the final conclusion.
```css
.stage3 {
  background: #ECFDF5;
  border: 1px solid #34D399;
}

.stage3 .stage-title {
  color: #065F46;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stage3 .stage-title::before {
  content: '✓';
  display: inline-block;
  background: #10B981;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  text-align: center;
  line-height: 20px;
  font-size: 14px;
}

.stage3 .markdown-content p {
  color: #064E3B;
  font-size: 1.05rem; /* Slightly larger text for the final answer */
}
```

- [ ] **Step 2: Commit**
```bash
git add frontend/src/components/Stage3.css
git commit -m "style: apply synthesis success styling to Stage 3"
```
