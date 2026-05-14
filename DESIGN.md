---
name: "Synapse Glass"
version: "1.0.0"
colors:
  # Dark Mode Foundation
  surface: "#080B11"
  surface-dim: "#0E131F"
  surface-bright: "#192233"
  surface-container: "#151D2E"
  surface-border: "#232F47"

  # Neural Synapse Accents
  primary: "#00E5FF"         # Vibrant Cyan - Synaptic Firing
  primary-glow: "rgba(0, 229, 255, 0.25)"
  secondary: "#7C4DFF"       # Deep Violet - Hidden Layers
  secondary-glow: "rgba(124, 77, 255, 0.25)"
  tertiary: "#FF3366"        # Hot Pink/Magenta - Error & Loss
  
  # Status Indicators
  success: "#00E676"         # High Accuracy
  warning: "#FFB300"         # Training Warning
  danger: "#FF1744"          # High Loss
  
  # Typography Colors
  text-primary: "#F8F9FA"
  text-secondary: "#A4B3C6"
  text-muted: "#677D98"

typography:
  display-lg:
    fontFamily: "Space Grotesk"
    fontSize: "48px"
    fontWeight: 700
    lineHeight: "56px"
    letterSpacing: "-0.03em"
  headline-md:
    fontFamily: "Space Grotesk"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: "36px"
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: "Inter"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "24px"
    letterSpacing: "0"
  code-sm:
    fontFamily: "JetBrains Mono"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: "20px"
    letterSpacing: "0"

rounded:
  sm: "4px"
  DEFAULT: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  full: "9999px"

elevation:
  sm: "0 2px 4px rgba(0,0,0,0.3)"
  md: "0 8px 16px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05)"
  lg: "0 16px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.08)"
  synapse: "0 0 30px rgba(0, 229, 255, 0.2), 0 8px 24px rgba(0,0,0,0.5)"

components:
  glass-panel:
    backgroundColor: "rgba(21, 29, 46, 0.6)"
    backdropFilter: "blur(12px)"
    border: "1px solid rgba(255, 255, 255, 0.08)"
    borderRadius: "{rounded.lg}"
    boxShadow: "{elevation.md}"
  
  synaptic-button:
    backgroundColor: "{colors.primary}"
    color: "{colors.surface}"
    borderRadius: "{rounded.full}"
    typography: "{typography.body-md}"
    fontWeight: 600
    boxShadow: "{elevation.sm}"
    transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
    hover:
      boxShadow: "{elevation.synapse}"
      transform: "translateY(-2px)"
---

# Synapse Glass Design System

Welcome to the **Synapse Glass** design system. This system is crafted specifically for advanced AI visualizers, neural network dashboards, and data-heavy machine learning applications. 

By establishing a strong connection between bio-neural networks and digital glassmorphism, Synapse Glass emphasizes depth, luminosity, and precision.

## ✨ Core Design Rationale

The visual system mirrors the conceptual flow of a neural network:
1. **Depth through Glass**: The use of dark, translucent glass panels represents layers of the network stacked atop one another.
2. **Vibrant Cyan (Synapses)**: Represents active forward propagation, high weights, and final correct classifications.
3. **Deep Violet (Processing)**: Denotes the mysterious "hidden layers" and complex feature extractions.
4. **Magenta (Entropy)**: Used sparingly to signify high-loss zones, computational heat, and gradient descent adjustments.

---

## 🎨 Visual Vocabulary

### Surfaces & Contrast
All interactive containers must utilize the `glass-panel` structure. 
- Avoid solid, opaque backgrounds for modules.
- Ensure the `backdropFilter: blur(12px)` is active to sustain readability over dynamic background particles or neural graphs.

### Typography Intent
- **Headers & Numerical Weights**: Use *Space Grotesk* to convey a scientific, futuristic tone.
- **Body & Descriptive Copy**: Use *Inter* for maximum readability in data metrics and tabular logs.
- **Code & Tensors**: Use *JetBrains Mono* for monospace matrix transformations and architecture code blocks.

---

## ✅ Do's and Don'ts

### Do
- **Do** use subtle neon glowing shadows (`elevation.synapse`) only for primary call-to-actions, high-confidence predictions, or currently firing hidden nodes.
- **Do** keep the background dark obsidian (`colors.surface`) to let data visualizations pop cleanly without causing ocular fatigue.
- **Do** utilize absolute rounded corners (`rounded.full`) for connection nodes in network visualizations.

### Don't
- **Don't** combine solid vibrant colors side-by-side. Maintain breathability via dark spacing.
- **Don't** use standard bright reds or basic blues; rely instead on our precise magenta (`colors.tertiary`) and violet (`colors.secondary`) tokens to ensure a premium visual experience.
- **Don't** use sharp 90-degree corners for UI windows. Synapse Glass requires smooth curvatures (`rounded.lg` or higher).
