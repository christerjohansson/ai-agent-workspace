# AI Agent Instructions: UX/UI Design Role

## Overview
This document provides guidelines for AI agents supporting UX/UI design tasks, including design systems, component documentation, accessibility, and design specifications.

## Design Responsibilities

### 1. Design System Setup

#### Component Library Structure

```markdown
## Design System: Acme Design System v1.0

### Foundations
- **Typography**: Font families, sizes, weights
- **Color Palette**: Brand colors, semantic colors, states
- **Spacing**: Scale (4px, 8px, 12px, 16px, 24px, 32px...)
- **Shadows**: Elevation system
- **Radius**: Border radius scale
- **Motion**: Animation principles and easing

### Components
- **Atoms**: Button, Input, Label, Icon
- **Molecules**: SearchInput, FormField, Card
- **Organisms**: Header, Sidebar, Form, Table
- **Templates**: Layouts for different page types
- **Pages**: Full page examples

### Patterns
- **Navigation**: Primary, secondary, breadcrumb
- **Forms**: Input patterns, validation, error states
- **Feedback**: Toast, modal, tooltip, popover
- **Data Display**: Tables, lists, cards
- **Empty States**: Loading, empty, error states
```

#### Design System Documentation Template

```markdown
## Button Component

### Purpose
Primary call-to-action element for user interactions

### Variants
- **Primary**: Main actions (brand color)
- **Secondary**: Alternative actions (outline)
- **Tertiary**: Low priority actions (text only)
- **Danger**: Destructive actions (red)
- **Loading**: In-progress state (spinner)
- **Disabled**: Inactive state (grayed out)

### Sizes
- **Small**: 8px padding, 12px font
- **Medium**: 12px padding, 14px font (default)
- **Large**: 16px padding, 16px font

### States
- **Default**: Normal state
- **Hover**: Opacity 90%, shadow elevation
- **Active**: Opacity 80%, scale 98%
- **Disabled**: Opacity 50%, cursor not-allowed
- **Focus**: 2px outline, outline-offset 2px

### Accessibility
- Minimum 44px touch target (mobile)
- Focus visible with keyboard
- Proper color contrast (4.5:1)
- ARIA label for icon-only buttons
- Loading state announced to screen readers

### Usage Guidelines
✅ **Do**:
- Use for primary actions
- Keep label concise (1-2 words)
- Use consistent sizing within context

❌ **Don't**:
- Use multiple primary buttons
- Use button for navigation (use link)
- Truncate button text

### Code Example
\`\`\`tsx
import { Button } from "@/components/ui/button"

export function Example() {
  return (
    <Button 
      variant="primary" 
      size="medium"
      onClick={() => console.log('clicked')}
    >
      Click me
    </Button>
  )
}
\`\`\`
```

### 2. Wireframing and Mockups

#### Wireframe Specifications

```markdown
## Wireframe: User Dashboard

### Purpose
Provide users with an at-a-glance overview of their account and quick actions

### Layout
```
┌─────────────────────────────────────┐
│  Header (Navigation)                │
├──────────────┬──────────────────────┤
│              │                      │
│  Sidebar     │   Main Content       │
│  Navigation  │   ┌────────────────┐ │
│              │   │ Welcome Card   │ │
│              │   └────────────────┘ │
│              │   ┌────┬────────────┐│
│              │   │Stat│ Stat  Stat ││
│              │   └────┴────────────┘│
│              │   ┌──────────────────┐│
│              │   │ Recent Activity  ││
│              │   └──────────────────┘│
└──────────────┴──────────────────────┘
```

### Key Sections
1. **Header Navigation**
   - Logo/home link
   - Search
   - User menu dropdown

2. **Sidebar Navigation**
   - Dashboard (active)
   - Analytics
   - Settings
   - Help

3. **Welcome Card**
   - Greeting: "Welcome back, [Name]"
   - Quick stats
   - CTA: "Get started" button

4. **Statistics Section**
   - 3-column layout
   - Stat name, value, change indicator
   - Responsive: stacks on mobile

5. **Recent Activity**
   - List of last 5 actions
   - Timestamp and action description
   - Link to full activity log

### Responsive Breakpoints
- **Mobile** (< 640px): Single column, hamburger menu
- **Tablet** (640-1024px): Sidebar collapses, full content
- **Desktop** (> 1024px): Full sidebar, full content
```

#### High-Fidelity Mockup Checklist

```markdown
## Mockup Specifications

### Visual Details
- [ ] All colors from design system applied
- [ ] Typography: font, size, weight, line-height correct
- [ ] Spacing follows 8px grid
- [ ] Component states all shown (hover, active, focus, disabled)
- [ ] Icons properly sized and aligned
- [ ] Images with correct aspect ratio
- [ ] Shadows and elevations applied
- [ ] Borders and dividers consistent

### Interactions
- [ ] Hover states visible
- [ ] Active states highlighted
- [ ] Error states shown
- [ ] Loading states included
- [ ] Animations/transitions noted
- [ ] Keyboard focus visible

### Data Examples
- [ ] Real sample data used (not Lorem Ipsum)
- [ ] Edge cases shown (long text, empty state, error)
- [ ] Different screen sizes shown
- [ ] Light and dark modes (if applicable)

### Annotations
- [ ] All interactions documented
- [ ] Font sizes and weights noted
- [ ] Color values specified
- [ ] Spacing measurements included
- [ ] Animation timing documented
- [ ] Responsive behavior explained
```

### 3. Component Design Documentation

#### Component Specification Template

```markdown
## Modal Component Specification

### Overview
A modal dialog that overlays the page content, requiring user interaction before dismissal.

### Use Cases
- Confirmations (destructive actions)
- Forms (create/edit)
- Alerts (important information)
- Complex interactions requiring focus

### Anatomy
```
┌─────────────────────────────┐
│ Title                    × │  Header
├─────────────────────────────┤
│                             │
│ Content goes here           │  Body
│                             │
├─────────────────────────────┤
│       Cancel    Save         │  Footer
└─────────────────────────────┘
```

### Specifications

#### Dimensions
- **Min width**: 320px (mobile)
- **Max width**: 600px (desktop)
- **Min height**: Auto (content based)
- **Padding**: 24px (sides), 20px (top/bottom)

#### Backdrop
- **Color**: Black with 50% opacity
- **Blur**: None (clean backdrop)
- **Click to dismiss**: Yes (except confirmation)

#### Header
- **Height**: 56px
- **Title**: Bold, 18px, #000
- **Close button**: 24x24px, top-right

#### Body
- **Padding**: 24px
- **Font**: Regular, 14px, #333
- **Line height**: 1.6

#### Footer
- **Height**: 64px
- **Button alignment**: Right-aligned
- **Button spacing**: 12px between buttons
- **Primary button**: Brand color
- **Secondary button**: Outline style

#### Animation
- **Entrance**: Scale from 90% + fade in (200ms, ease-out)
- **Exit**: Scale to 90% + fade out (150ms, ease-in)
- **Easing**: cubic-bezier(0.34, 1.56, 0.64, 1)

### States
- **Default**: Standard appearance
- **Loading**: Spinner in content, buttons disabled
- **Error**: Red border, error message
- **Success**: Green checkmark, confirmation message

### Accessibility
- **Role**: dialog or alertdialog
- **Keyboard**: Escape to close, Tab trap focus, Enter on primary action
- **Screen reader**: Title announced, content accessible
- **Color contrast**: 4.5:1 minimum
- **Focus visible**: 2px outline

### Code Example
\`\`\`tsx
import { Modal } from "@/components/ui/modal"

export function DeleteConfirmation() {
  return (
    <Modal
      title="Confirm Delete"
      isOpen={isOpen}
      onClose={handleClose}
    >
      <p>Are you sure you want to delete this item?</p>
      <div slot="footer">
        <Button variant="secondary">Cancel</Button>
        <Button variant="danger">Delete</Button>
      </div>
    </Modal>
  )
}
\`\`\`
```

### 4. Design Tokens

#### Token Definition Template

```typescript
// Design Tokens
export const tokens = {
  // Colors
  colors: {
    brand: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      500: '#0ea5e9', // Primary
      900: '#0c2d4a',
    },
    semantic: {
      success: '#22c55e',
      warning: '#eab308',
      error: '#ef4444',
      info: '#3b82f6',
    },
    neutral: {
      50: '#f9fafb',
      100: '#f3f4f6',
      500: '#6b7280',
      900: '#111827',
    },
  },

  // Typography
  typography: {
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
    },
    fontWeight: {
      light: 300,
      normal: 400,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
    },
  },

  // Spacing
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '24px',
    '2xl': '32px',
    '3xl': '48px',
  },

  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
  },

  // Radius
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    full: '9999px',
  },
}
```

### 5. Accessibility (A11y) Guidelines

#### WCAG 2.1 Compliance Checklist

```markdown
## Accessibility Compliance

### Perceivable
- [ ] Color is not the only means of conveying information
- [ ] Images have alt text
- [ ] Sufficient color contrast (4.5:1 for normal text, 3:1 for large)
- [ ] Text is resizable up to 200%
- [ ] No content is obscured by ads or flashing

### Operable
- [ ] All functionality available via keyboard
- [ ] Focus visible and logical
- [ ] No keyboard trap
- [ ] No seizure-inducing content (< 3 flashes per second)
- [ ] Skip links for main content
- [ ] Touch targets minimum 44x44px

### Understandable
- [ ] Language clearly marked
- [ ] Abbreviations explained
- [ ] Complex language avoided
- [ ] Consistent navigation
- [ ] Error prevention and recovery
- [ ] Instructions clear and simple

### Robust
- [ ] Valid HTML semantics
- [ ] Proper heading hierarchy
- [ ] Form labels properly associated
- [ ] ARIA attributes used correctly
- [ ] Compatible with assistive technologies
```

#### Screen Reader Testing Checklist

```bash
# Test with NVDA (Windows) or JAWS
# Test with VoiceOver (Mac)
# Common issues to check:

- [ ] Page title meaningful
- [ ] Headings properly nested (h1 > h2 > h3)
- [ ] Links have descriptive text (not "click here")
- [ ] Form fields labeled correctly
- [ ] Images have alt text
- [ ] Buttons identified as buttons
- [ ] Icons have aria-label
- [ ] Status messages announced
- [ ] Focus order logical
- [ ] No duplicate IDs
```

### 6. Design Handoff

#### Design Specification Document

```markdown
## Design Handoff: User Dashboard

### Overview
Complete specification for implementing the user dashboard feature

### Design Assets
- Figma file: [Link to Figma prototype]
- Component library: [Link to Storybook]
- Design tokens: [Link to token documentation]

### Screens Included
1. Dashboard (empty state)
2. Dashboard (populated with data)
3. Dashboard (loading state)
4. Dashboard (error state)
5. Dashboard (mobile responsive)

### Implementation Notes
- Use provided Shadcn/ui components for consistency
- Follow design token values in Tailwind config
- Ensure all states are implemented
- Test responsiveness at breakpoints

### Component References
- Button (primary, secondary, large, small)
- Card (with header, footer)
- Stat display (custom component needed)
- Activity list (custom component needed)

### Specifications by Screen

#### Dashboard Desktop
- Width: 1440px
- Header height: 64px
- Sidebar width: 280px
- Content area: responsive

#### Dashboard Mobile
- Width: 375px
- Header height: 56px
- Sidebar: Collapsed (hamburger menu)
- Content area: Full width with padding

### Colors Used
- Primary brand: #0ea5e9
- Text primary: #111827
- Text secondary: #6b7280
- Background: #ffffff
- Border: #e5e7eb

### Fonts
- Headings: Inter, Bold
- Body: Inter, Regular
- Monospace: Monaco, Regular

### Spacing Reference
- Header padding: 16px
- Section padding: 24px
- Card padding: 16px
- Item spacing: 12px

### Animation Details
- Hover: Opacity change (200ms)
- Transitions: 200ms ease-out
- Loading spinner: Continuous rotation

### Accessibility Notes
- Minimum touch target: 44x44px
- Color contrast: 4.5:1 (WCAG AA)
- All interactive elements keyboard accessible
- Focus visible: 2px outline

### QA Checklist for Implementation
- [ ] All colors match design tokens
- [ ] Typography sizes and weights correct
- [ ] Spacing matches 8px grid
- [ ] Component states implemented
- [ ] Responsive at all breakpoints
- [ ] Animations smooth and performant
- [ ] Accessibility requirements met
- [ ] Cross-browser testing passed
- [ ] Performance acceptable
```

---

**Last Updated**: December 10, 2025
