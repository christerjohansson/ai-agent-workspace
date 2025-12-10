# AI Agent Instructions: NextJS + TypeScript + React + Tailwind Setup

## Overview
This document provides step-by-step instructions for AI agents to create and configure a modern Next.js project with TypeScript, React, Tailwind CSS, and Shadcn/ui component library.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager available
- Access to terminal/command line

## Step 1: Create Next.js Project

```bash
npx create-next-app@latest my-agentic-app --typescript --eslint --tailwind --app
```

**Interactive Prompts - Select:**
- ✅ TypeScript: Yes
- ✅ ESLint: Yes
- ✅ Tailwind CSS: Yes
- ✅ Use src/ directory: Yes (recommended)
- ✅ App Router: Yes (default)
- ✅ Import alias: Yes (use @/*)
- ✅ Turbopack: No (optional, but improves dev experience)

## Step 2: Navigate to Project

```bash
cd my-agentic-app
```

## Step 3: Install Shadcn/ui (Most Common Component Library)

Shadcn/ui is the recommended component library as it provides:
- Pre-built, accessible React components
- Built on Radix UI and Tailwind CSS
- Copy-paste code approach (fully customizable)
- Zero runtime dependencies
- TypeScript-first

### Initialize Shadcn/ui

```bash
npx shadcn-ui@latest init
```

**Configuration:**
- Style: New York (or your preference)
- Base color: Slate (or your preference)
- CSS variables: Yes

## Step 4: Install Common Components

Install the most frequently used Shadcn/ui components:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add select
npx shadcn-ui@latest add textarea
npx shadcn-ui@latest add form
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add tooltip
npx shadcn-ui@latest add navbar
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add accordion
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add breadcrumb
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add radio-group
npx shadcn-ui@latest add slider
npx shadcn-ui@latest add switch
```

### Or Add All at Once

```bash
npx shadcn-ui@latest add --all
```

## Step 5: Verify Installation

```bash
npm run dev
```

Visit `http://localhost:3000` to confirm the development server is running.

## Project Structure

After setup, your project structure should look like:

```
my-agentic-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── ui/              # Shadcn/ui components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── input.tsx
│   │       └── ...
│   └── lib/
│       └── utils.ts         # Utility functions (cn for classname merging)
├── public/
├── .env.local
├── .gitignore
├── next.config.ts
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Key Files Explained

### `next.config.ts`
Configuration file for Next.js build and runtime settings.

### `tailwind.config.ts`
Tailwind CSS configuration with color variables and custom settings.

### `src/app/globals.css`
Global styles using Tailwind directives and CSS variables for theming.

### `src/lib/utils.ts`
Utility functions, primarily the `cn()` function for merging Tailwind classes:

```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Common Development Tasks

### Create a New Page

```bash
# Create app/dashboard/page.tsx
```

```typescript
export default function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-4">Dashboard</h1>
      {/* Your content */}
    </div>
  )
}
```

### Create a Reusable Component

```bash
# Create src/components/MyComponent.tsx
```

```typescript
import { Button } from "@/components/ui/button"

interface MyComponentProps {
  title: string
  onAction?: () => void
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <div className="p-4 border rounded-lg">
      <h2 className="text-2xl font-semibold mb-2">{title}</h2>
      <Button onClick={onAction}>Click me</Button>
    </div>
  )
}
```

### Use Shadcn/ui Components

```typescript
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Example Card</CardTitle>
        <CardDescription>This is a Shadcn/ui card component</CardDescription>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

## Useful NPM Scripts

```bash
# Development
npm run dev          # Start dev server on port 3000

# Production
npm run build        # Build for production
npm run start        # Start production server

# Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking

# Development utilities
npm run format       # Format code (if Prettier is configured)
npm run test         # Run tests (if testing framework is installed)
```

## Adding Additional Tools (Optional)

### Add React Query (Data Fetching)
```bash
npm install @tanstack/react-query
```

### Add Zod (Schema Validation)
```bash
npm install zod
```

### Add React Hook Form (Form Management)
```bash
npm install react-hook-form
```

### Add Authentication (NextAuth.js)
```bash
npm install next-auth
```

### Add Prisma (Database ORM)
```bash
npm install @prisma/client
npm install -D prisma
npx prisma init
```

## Environment Variables

Create `.env.local` file in the root:

```env
# API endpoints
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# Database (if using Prisma)
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Authentication secrets
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

## Troubleshooting

### Port 3000 Already in Use
```bash
npm run dev -- -p 3001  # Use different port
```

### Shadcn/ui Components Not Found
```bash
# Ensure the component is properly installed
npx shadcn-ui@latest add button

# Clear Next.js cache
rm -r .next
npm run dev
```

### TypeScript Errors
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Regenerate TypeScript definitions
rm -r node_modules/.cache
npm run build
```

## Best Practices

1. **Use TypeScript**: Leverage full type safety with interfaces and types
2. **Component-Driven**: Break UI into reusable Shadcn/ui components
3. **Utility Classes**: Use Tailwind's utility classes instead of CSS files
4. **Dark Mode**: Leverage Shadcn/ui's built-in dark mode support
5. **Responsive Design**: Use Tailwind breakpoints (sm, md, lg, xl, 2xl)
6. **CSS Variables**: Use theme variables for consistent styling
7. **Code Organization**: Keep components in `src/components`, utilities in `src/lib`

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Shadcn/ui Documentation](https://ui.shadcn.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

## Notes for AI Agents

When executing these instructions:
1. Always verify Node.js version is 18 or higher: `node --version`
2. Use `npm` unless the user specifies `yarn` or `pnpm`
3. When installing components, do it interactively or use `--yes` flag
4. Verify each step completes successfully before proceeding
5. Check for any peer dependency warnings and address them
6. Test the development server starts without errors on port 3000
7. Confirm the project structure matches the documented layout

---

**Last Updated**: December 10, 2025
**Compatible With**: Next.js 14+, React 18+, Tailwind CSS 3+, Shadcn/ui latest
