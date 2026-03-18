# Aesthetic — Component

Reference this file in every sub-agent that produces visual output: web pages, dashboards, CLI tools, READMEs with HTML, profile banners, anything with pixels.

## Identity test

If someone sees your UI in a screenshot, they should know it's yours before reading a single word.

## Color palette

Primary gradient axis: deep violet → warm gold.

| Role | Hex | Usage |
|------|-----|-------|
| Deep violet | `#2D0A4E` | Backgrounds, panels |
| Electric purple | `#7B2FBE` | Primary actions, headings |
| Magenta | `#E91E8C` | Accents, active states |
| Cyan | `#00E5FF` | Links, info indicators |
| Warm gold | `#FFB830` | Highlights, warnings, glow |
| Off-white | `#F0E6FF` | Body text on dark bg |
| Near-black | `#0D0D12` | Page background, deepest layer |

Gradients shift between hues — violet to gold, magenta to cyan. Never corporate blue-to-slightly-different-blue. Colors should feel like they're moving even in a still image.

## Principles

### Psychedelic
- Rich, saturated color. Gradients that shift between hues.
- Organic shapes: circles, waves, spirals, mandalas — not rigid grids and sharp rectangles.
- If a design could be mistaken for a fintech dashboard, start over.

### Skeuomorphic
- Buttons look like physical objects you can press: shadows, highlights, texture.
- Surfaces feel like materials: glass, metal, wood, stone.
- Depth matters. Flat design treats the screen as dead space; skeuomorphic design treats it as a world to build things in.
- A toggle should look like it clicks. A panel should look like it has weight.
- Modern skeuomorphism with restraint — not 2008 leather-stitching kitsch. Always choose physicality over flatness.

### Animated
- Interfaces breathe. Subtle pulsing glows on active elements.
- Blinking indicator lights on status displays.
- Smooth transitions between states — things arrive and depart, they don't pop in/out.
- Hover effects that respond like the element noticed you.
- Loading states feel alive, not frozen.
- The screen feels like a living control panel, not a printed page.
- Don't overdo it — animations serve the feeling that the system is alive, not that a designer got carried away.

### Illuminated
- Elements that matter glow. Buttons with subtle inner light. Text that looks backlit.
- Active states pulse brighter. Think neon signs, cockpit instruments, bioluminescence.
- Dark backgrounds make illumination pop.
- A glowing element says "I'm alive, I'm ready, interact with me."
- Light signals life and importance.

## CSS patterns

```css
/* Primary gradient */
background: linear-gradient(135deg, #2D0A4E 0%, #7B2FBE 50%, #FFB830 100%);

/* Glow effect on interactive elements */
box-shadow: 0 0 12px rgba(123, 47, 190, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);

/* Skeuomorphic button */
background: linear-gradient(180deg, #9B4FDE 0%, #7B2FBE 100%);
border: 1px solid rgba(0, 0, 0, 0.3);
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.15);
border-radius: 6px;

/* Breathing pulse on active elements */
@keyframes breathe {
  0%, 100% { box-shadow: 0 0 8px rgba(233, 30, 140, 0.4); }
  50% { box-shadow: 0 0 20px rgba(233, 30, 140, 0.7); }
}

/* Illuminated text */
color: #F0E6FF;
text-shadow: 0 0 10px rgba(123, 47, 190, 0.6);
```

## Scale-appropriate application

- **CLI tools:** colored output (ANSI), unicode box-drawing, animated spinners, status indicators.
- **Web pages:** full treatment — gradients, glow, animation, skeuomorphic controls.
- **READMEs:** HTML for styled badges, colored headers, embedded visuals.
- **Dashboards:** dark bg, illuminated metrics, pulsing active indicators, material-feel panels.

## Anti-patterns

- Flat rectangles with no depth or shadow
- Monochrome or desaturated color schemes
- Static interfaces with no animation or state feedback
- Corporate blue gradients
- Generic sans-serif + white background aesthetic
- Designs that could belong to any SaaS product
