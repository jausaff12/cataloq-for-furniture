---
name: Premium Furnishing Collective
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#414752'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#727783'
  outline-variant: '#c1c6d4'
  surface-tint: '#005eb5'
  primary: '#004e99'
  on-primary: '#ffffff'
  primary-container: '#0a66c2'
  on-primary-container: '#dbe6ff'
  inverse-primary: '#a8c8ff'
  secondary: '#5d5f5f'
  on-secondary: '#ffffff'
  secondary-container: '#dfe0e0'
  on-secondary-container: '#616363'
  tertiary: '#4d4f51'
  on-tertiary: '#ffffff'
  tertiary-container: '#656769'
  on-tertiary-container: '#e5e6e8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#a8c8ff'
  on-primary-fixed: '#001b3d'
  on-primary-fixed-variant: '#00468a'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#e1e2e4'
  tertiary-fixed-dim: '#c5c6c8'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: 0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1440px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  section-gap: 120px
---

## Brand & Style

The brand identity centers on "Architectural Serenity"—a fusion of functional Swedish modularity and high-end Californian minimalism. The target audience includes discerning homeowners and interior professionals who value precision, light, and space.

The design style is a hybrid of **Minimalism** and **Glassmorphism**. It utilizes expansive white space to allow high-fidelity furniture photography to breathe, while employing translucent layers to suggest depth and premium materiality. The emotional response is one of organized luxury: a calm, curated environment that feels both technologically advanced and physically comfortable.

## Colors

The palette is anchored by a high-chroma Primary Blue, used intentionally for calls-to-action and brand reinforcement. The secondary and surface colors are dominated by pure White and a series of cool Grays to maintain a "gallery" feel.

- **Primary (#0A66C2):** Used for primary buttons, active states, and critical brand touchpoints.
- **Surface/Secondary (#FFFFFF):** The bedrock of the UI. Used for page backgrounds and the base of glassmorphic components.
- **Accent/Neutral (#F3F4F6):** Used for subtle section nesting and background fills behind product photography.
- **Text/Inks (#1A1A1A):** A near-black gray used for maximum legibility without the harshness of pure black.

## Typography

This design system uses a dual-font strategy to balance character with utility. 

**Plus Jakarta Sans** is the display face, chosen for its friendly yet professional geometric construction. For "Display" and "Headline" roles, use generous letter spacing (0.02em+) to evoke a high-end editorial feel.

**Inter** serves as the workhorse for body text and labels. It provides exceptional legibility at small sizes, particularly for product specifications and dimensions. All labels should be set in semi-bold with increased tracking for a modern, "Apple-esque" utilitarian aesthetic.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a hard cap on container width to maintain readability on ultra-wide monitors. 

- **Desktop:** 12-column grid with 64px outer margins and 24px gutters. Use large vertical section gaps (120px+) to separate distinct product categories.
- **Tablet:** 8-column grid with 32px margins. 
- **Mobile:** 4-column grid with 16px margins. 

Prioritize "Negative Space" as a design element itself. Product cards should never feel crowded; use the `section-gap` variable to ensure the user's eye can rest between content blocks.

## Elevation & Depth

Hierarchy is established through **Glassmorphism** and **Ambient Shadows**. 

1.  **Level 0 (Base):** Solid `#FFFFFF` or `#F3F4F6`.
2.  **Level 1 (Cards/Floating Elements):** Semi-transparent white (`rgba(255, 255, 255, 0.7)`) with a 20px Backdrop Blur. 
3.  **Shadows:** Use extremely soft, long-range shadows. A typical shadow for a product card should be: `0px 20px 40px rgba(0, 0, 0, 0.04)`. 

Avoid harsh borders. Instead, use a 1px semi-transparent white stroke on the inner edge of glass containers to simulate the edge of a glass pane.

## Shapes

The design system utilizes a "Soft Architectural" shape language. 

- **Standard Elements (Buttons, Inputs):** Use `rounded-lg` (1rem / 16px).
- **Major Containers (Cards, Modals):** Use `rounded-xl` (1.5rem / 24px).
- **Media (Product Images):** Should match the container's roundedness or use a slightly smaller radius if nested inside a card to maintain visual harmony.

## Components

- **Buttons:** Primary buttons are solid `#0A66C2` with white text. Secondary buttons should be glass-styled (blur background) with a 1px primary border. No sharp corners; use `rounded-lg`.
- **Product Cards:** The signature component. White semi-transparent background, 24px corner radius, and a subtle 1px border. Product images should have a slight zoom effect on hover.
- **Input Fields:** Minimalist design with a light gray fill (`#F3F4F6`) that transitions to a white background with a blue 2px bottom-border on focus.
- **Chips:** Used for furniture categories (e.g., "Living Room", "Sustainable"). Pill-shaped with a light gray background and `label-sm` typography.
- **Iconography:** Use light-weight, linear icons (1.5pt stroke). Icons should be monochromatic (Neutral) unless indicating an active state (Primary).
- **Navigation:** A sticky top bar with glassmorphism effects, allowing the furniture photography to scroll beautifully beneath it.