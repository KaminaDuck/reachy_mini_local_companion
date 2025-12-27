---
title: "Material-UI (MUI) v7 Component Library"
description: "Material-UI React component library implementing Material Design with theming and styling"
type: "framework-guide"
tags: ["mui", "material-ui", "react", "components", "material-design", "theming", "ui-library", "typescript"]
category: "frontend"
subcategory: "ui-libraries"
version: "7.3.4"
last_updated: "2025-11-01"
status: "stable"
sources:
  - name: "Material-UI Documentation"
    url: "https://mui.com/material-ui/"
  - name: "Material-UI Getting Started"
    url: "https://mui.com/material-ui/getting-started/"
  - name: "Material-UI Theming"
    url: "https://mui.com/material-ui/customization/theming/"
  - name: "Material-UI Customization"
    url: "https://mui.com/material-ui/customization/how-to-customize/"
  - name: "MUI npm Package"
    url: "https://www.npmjs.com/package/@mui/material"
related: ["../react/react-19.md", "../vite/vite-7.md"]
author: "unknown"
contributors: []
---

# Material-UI (MUI) v7 Component Library

Material-UI (MUI) is a comprehensive React component library that implements Google's Material Design system. ([Material-UI Documentation][1]) The library enables developers to build user interfaces following established design principles. ([Material-UI Documentation][1])

## Overview

Material-UI is now called MUI and uses the `@mui/material` package name (not `@material-ui/core`, which is the older v4). ([MUI npm Package][5]) MUI provides pre-built, production-ready React components including buttons, forms, navigation elements, dialogs, and data display components that follow Material Design standards. ([Material-UI Documentation][1])

### Current Version

Version 7.3.4 is the reference version for this guide, representing the latest stable release with full TypeScript support and modern React compatibility.

### Design Principles

Material-UI adheres to Material Design's core tenets: ([Material-UI Documentation][1])
- Elevation and depth through shadows
- Responsive layouts and mobile-first approach
- Clear visual hierarchy and typography
- Consistent spacing and alignment grids

## Requirements

**Peer Dependencies**: React and react-dom are peer dependencies, with support for "react": "^17.0.0 || ^18.0.0 || ^19.0.0". ([MUI npm Package][5])

## Installation

### Basic Installation

To install Material UI, run: ([MUI npm Package][5])

```bash
npm install @mui/material @emotion/react @emotion/styled
```

**Styling Engine**: Material UI uses Emotion as its default styling engine, which is why `@emotion/react` and `@emotion/styled` are included in the installation command. ([MUI npm Package][5])

### Alternative with styled-components

If you want to use styled-components instead: ([MUI npm Package][5])

```bash
npm install @mui/material @mui/styled-engine-sc styled-components
```

### Optional Packages

**Material Icons**: To use the font Icon component or prebuilt SVG Material Icons, install the Material Icons font via npm or Google Web Fonts CDN. ([MUI npm Package][5])

```bash
# Font icons
npm install @mui/icons-material

# Or use Google Fonts CDN in HTML
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/icon?family=Material+Icons"
/>
```

**Roboto Font**: Material Design uses Roboto font by default:

```html
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
/>
```

## Core Concepts

### Component Library

MUI provides extensive UI components: ([Material-UI Documentation][1])

**Input Components**:
- Button, ButtonGroup
- Checkbox, Radio, Switch
- TextField, Select, Autocomplete
- Slider, Rating

**Navigation**:
- AppBar, Toolbar
- Drawer, Menu
- Tabs, BottomNavigation
- Breadcrumbs, Pagination

**Data Display**:
- Avatar, Badge, Chip
- List, Table, DataGrid
- Card, Paper
- Typography, Divider
- Tooltip

**Feedback**:
- Alert, Snackbar
- Dialog, Modal
- Progress (Linear, Circular)
- Backdrop, Skeleton

**Surfaces**:
- Accordion
- Card, Paper
- AppBar

**Layout**:
- Box, Container
- Grid, Stack
- ImageList

### Design System

The library includes comprehensive theming capabilities with customizable color palettes, typography scales, spacing systems, and shadow definitions for consistent visual design. ([Material-UI Documentation][1])

The theming system uses CSS custom properties (variables) organized hierarchically: ([Material-UI Theming][3])

- **Spacing**: `--mui-spacing: 8px` serves as the base unit
- **Shape**: `--mui-shape-borderRadius: 4px` defines default border radius
- **Shadows**: 24 elevation levels (`--mui-shadows-0` through `--mui-shadows-24`)
- **Z-Index**: Layering system for modals, drawers, tooltips, etc.

### Accessibility

Components are built with accessibility in mind, supporting keyboard navigation, screen readers, and ARIA attributes for inclusive user experiences. ([Material-UI Documentation][1])

## Getting Started

### Basic Usage

Import components and use them in your React application:

```tsx
import React from 'react';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

function App() {
  return (
    <Stack spacing={2} direction="row">
      <Button variant="text">Text</Button>
      <Button variant="contained">Contained</Button>
      <Button variant="outlined">Outlined</Button>
    </Stack>
  );
}

export default App;
```

### With TypeScript

MUI has full TypeScript support:

```tsx
import { Button, ButtonProps } from '@mui/material';

interface CustomButtonProps extends ButtonProps {
  customProp?: string;
}

const CustomButton: React.FC<CustomButtonProps> = ({
  customProp,
  ...props
}) => {
  return <Button {...props} />;
};
```

## Theming

### Theme Structure

The theme defines comprehensive color variables: ([Material-UI Theming][3])

**Light Mode** includes:
- Primary, secondary, error, warning, info, and success colors with variants (light, dark, main)
- Text colors with primary, secondary, disabled, and tertiary levels
- Background and action state colors
- Component-specific overrides (Alert, Button, Chip, etc.)

**Dark Mode** automatically adjusts all palette variables for appropriate contrast and visibility. ([Material-UI Theming][3])

### Creating a Theme

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
      contrastText: '#fff',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
      contrastText: '#fff',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
  },
  spacing: 8, // Base spacing unit
  shape: {
    borderRadius: 4,
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Your app */}
    </ThemeProvider>
  );
}
```

### Dark Mode Support

The system uses `[data-mui-color-scheme="dark"]` selectors to provide comprehensive dark theme alternatives. ([Material-UI Theming][3])

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { useState } from 'react';

function App() {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const theme = createTheme({
    palette: {
      mode,
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* Your app */}
    </ThemeProvider>
  );
}
```

### Typography System

The theme includes CSS font variables defining styles for headings (h1-h6), body text, buttons, and captions. ([Material-UI Theming][3])

```tsx
const theme = createTheme({
  typography: {
    h1: { fontSize: '2.5rem', fontWeight: 500 },
    h2: { fontSize: '2rem', fontWeight: 500 },
    h3: { fontSize: '1.75rem', fontWeight: 500 },
    h4: { fontSize: '1.5rem', fontWeight: 500 },
    h5: { fontSize: '1.25rem', fontWeight: 500 },
    h6: { fontSize: '1rem', fontWeight: 500 },
    body1: { fontSize: '1rem', lineHeight: 1.5 },
    body2: { fontSize: '0.875rem', lineHeight: 1.43 },
    button: { fontSize: '0.875rem', fontWeight: 500, textTransform: 'uppercase' },
    caption: { fontSize: '0.75rem', lineHeight: 1.66 },
  },
});
```

## Customization Approaches

Material-UI offers multiple styling methods. ([Material-UI Customization][4])

### 1. The sx Prop

The sx prop lets you work with a superset of CSS that packages all of the style functions exposed in @mui/system. ([Material-UI Customization][4]) You can specify any valid CSS using this prop, as well as many theme-aware properties. ([Material-UI Customization][4])

The sx prop is the best option for adding style overrides to a single instance of a component in most cases. ([Material-UI Customization][4])

```tsx
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function Example() {
  return (
    <Box
      sx={{
        width: 300,
        height: 200,
        backgroundColor: 'primary.main',
        '&:hover': {
          backgroundColor: 'primary.dark',
        },
        padding: 2, // Uses theme spacing (2 * 8px = 16px)
        borderRadius: 1, // Uses theme shape
      }}
    >
      <Button
        sx={{
          color: 'white',
          fontWeight: 'bold',
          textTransform: 'none',
        }}
      >
        Custom Button
      </Button>
    </Box>
  );
}
```

**Theme-aware properties**:
```tsx
<Box
  sx={{
    // Spacing
    p: 2,          // padding: theme.spacing(2)
    m: 1,          // margin: theme.spacing(1)
    pt: 3,         // paddingTop: theme.spacing(3)

    // Colors
    color: 'primary.main',
    bgcolor: 'background.paper',

    // Typography
    fontSize: 'h6.fontSize',
    fontWeight: 'fontWeightBold',

    // Responsive
    width: { xs: '100%', sm: '50%', md: '33%' },
  }}
/>
```

### 2. Styled API

The styled utility can be used as a replacement for emotion's or styled-components' styled() utility. ([Material-UI Customization][4]) Styled API creates custom components with styles that provide theme values, offering more control and flexibility. ([Material-UI Customization][4])

```tsx
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';

const CustomButton = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.primary.contrastText,
  padding: theme.spacing(1, 3),
  borderRadius: theme.shape.borderRadius * 2,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
  '&.Mui-disabled': {
    backgroundColor: theme.palette.action.disabledBackground,
  },
}));

function App() {
  return <CustomButton>Styled Button</CustomButton>;
}
```

**With props**:
```tsx
interface CustomBoxProps {
  featured?: boolean;
}

const CustomBox = styled(Box)<CustomBoxProps>(({ theme, featured }) => ({
  padding: theme.spacing(2),
  backgroundColor: featured
    ? theme.palette.primary.main
    : theme.palette.background.paper,
  border: `1px solid ${theme.palette.divider}`,
}));
```

### 3. Theme Component Customization

You can customize a component's styles, default props, and more by using its component key inside the theme. ([Material-UI Customization][4])

```tsx
const theme = createTheme({
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
      defaultProps: {
        disableElevation: true,
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        size: 'small',
      },
    },
  },
});
```

**Using sx in theme**:
You can use the sx prop inside the styleOverrides key to modify styles within the theme using shorthand CSS notation. ([Material-UI Customization][4])

```tsx
const theme = createTheme({
  components: {
    MuiChip: {
      styleOverrides: {
        root: ({ theme }) => ({
          sx: {
            px: 1,
            py: 0.5,
            borderRadius: 1,
          },
        }),
      },
    },
  },
});
```

### 4. Global CSS Override

```tsx
import { GlobalStyles } from '@mui/material';

function App() {
  return (
    <>
      <GlobalStyles
        styles={{
          '*': {
            boxSizing: 'border-box',
          },
          body: {
            margin: 0,
            padding: 0,
          },
        }}
      />
      {/* Your app */}
    </>
  );
}
```

## Best Practices

### Styling Strategy

Use the sx prop for simple customizations: If you're making minor tweaks to an MUI component, the sx prop is the way to go. For complex components, consider using the styled API to create reusable, custom-styled components. ([Material-UI Customization][4])

**When to use each approach**:

1. **sx prop**: Single-use customizations, responsive styles, quick prototyping
2. **styled()**: Reusable custom components, complex styling logic, performance-critical components
3. **Theme overrides**: Application-wide defaults, consistent component behavior
4. **Global styles**: CSS resets, body styles, font imports

### Component Organization

```tsx
// Good: Separate styled components
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(2),
}));

function MyComponent() {
  return (
    <StyledPaper>
      <Typography variant="h5">Title</Typography>
    </StyledPaper>
  );
}

// Avoid: Inline styles for reusable patterns
function MyComponent() {
  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Typography variant="h5">Title</Typography>
    </Paper>
  );
}
```

### Theme Organization

```tsx
// theme/palette.ts
export const palette = {
  primary: { main: '#1976d2' },
  secondary: { main: '#9c27b0' },
};

// theme/typography.ts
export const typography = {
  fontFamily: 'Roboto, Arial, sans-serif',
  h1: { fontSize: '2.5rem' },
};

// theme/components.ts
export const components = {
  MuiButton: {
    styleOverrides: {
      root: { textTransform: 'none' },
    },
  },
};

// theme/index.ts
import { createTheme } from '@mui/material/styles';
import { palette } from './palette';
import { typography } from './typography';
import { components } from './components';

export const theme = createTheme({
  palette,
  typography,
  components,
});
```

### Performance Optimization

1. **Use theme caching**: Create theme outside component to avoid recreation
2. **Memoize styled components**: Define styled components outside render
3. **Avoid sx for static styles**: Use styled() for unchanging styles
4. **Leverage CSS-in-JS optimization**: Emotion handles style deduplication

```tsx
// Good: Theme created once
const theme = createTheme({ /* config */ });

function App() {
  return <ThemeProvider theme={theme}>...</ThemeProvider>;
}

// Avoid: Theme recreated on each render
function App() {
  const theme = createTheme({ /* config */ });
  return <ThemeProvider theme={theme}>...</ThemeProvider>;
}
```

### Accessibility

1. **Use semantic HTML**: MUI components use proper HTML elements
2. **Provide labels**: Always add labels to form inputs
3. **Keyboard navigation**: Ensure all interactive elements are keyboard accessible
4. **Color contrast**: Test theme colors for WCAG compliance
5. **ARIA attributes**: Use MUI's built-in ARIA support

```tsx
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function Form() {
  return (
    <form>
      <TextField
        label="Email"
        type="email"
        required
        helperText="Enter your email address"
        aria-describedby="email-helper-text"
      />
      <Button
        type="submit"
        aria-label="Submit form"
      >
        Submit
      </Button>
    </form>
  );
}
```

### Responsive Design

```tsx
import { useTheme, useMediaQuery } from '@mui/material';
import Box from '@mui/material/Box';

function ResponsiveComponent() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));

  return (
    <Box
      sx={{
        // Responsive spacing
        p: { xs: 1, sm: 2, md: 3 },

        // Responsive layout
        display: 'flex',
        flexDirection: { xs: 'column', md: 'row' },

        // Responsive typography
        fontSize: { xs: '0.875rem', sm: '1rem', md: '1.125rem' },
      }}
    >
      {isMobile ? 'Mobile View' : 'Desktop View'}
    </Box>
  );
}
```

## Common Patterns

### Layout with Grid

**Note**: In MUI v7, the Grid component (formerly Grid2 in v5-v6) is the current API. The old Grid v1 is now available as GridLegacy. For comprehensive Grid documentation, see [grid-component.md](grid-component.md).

```tsx
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

function Dashboard() {
  return (
    <Grid container spacing={3}>
      <Grid size={{ xs: 12, sm: 6, md: 4 }}>
        <Card>
          <CardContent>Card 1</CardContent>
        </Card>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 4 }}>
        <Card>
          <CardContent>Card 2</CardContent>
        </Card>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 4 }}>
        <Card>
          <CardContent>Card 3</CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
```

### Forms with Validation

```tsx
import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.includes('@')) {
      setError('Invalid email');
      return;
    }
    // Submit form
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing={2}>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={!!error}
          helperText={error}
          required
        />
        <Button type="submit" variant="contained">
          Login
        </Button>
      </Stack>
    </form>
  );
}
```

### Modal Dialog

```tsx
import { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';

function ConfirmDialog() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Open Dialog</Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Confirm Action</DialogTitle>
        <DialogContent>
          Are you sure you want to proceed?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={() => setOpen(false)} variant="contained">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
```

### Navigation with AppBar

```tsx
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

function Navigation() {
  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          My App
        </Typography>
        <Button color="inherit">Login</Button>
      </Toolbar>
    </AppBar>
  );
}
```

## MUI Ecosystem

The library operates within a broader MUI ecosystem: ([Material-UI Documentation][1])

- **MUI System**: Styling utilities and theming infrastructure
- **MUI X**: Advanced components for data grids and date picking
- **Documentation**: Comprehensive guides and interactive examples
- **Dark Mode Support**: Built-in theming for light and dark color schemes

### MUI X Components

Advanced components available separately:

```bash
npm install @mui/x-data-grid
npm install @mui/x-date-pickers
npm install @mui/x-charts
```

**DataGrid Example** (Note: DataGrid is separate from the Grid layout component):
```tsx
import { DataGrid } from '@mui/x-data-grid';

const columns = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'name', headerName: 'Name', width: 150 },
];

const rows = [
  { id: 1, name: 'John' },
  { id: 2, name: 'Jane' },
];

function DataTable() {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      pageSize={5}
    />
  );
}
```

## Troubleshooting

### Common Issues

**Issue**: Styles not applying

**Solution**: Ensure ThemeProvider wraps your app and CssBaseline is included:
```tsx
import { ThemeProvider, CssBaseline } from '@mui/material';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {/* Your app */}
    </ThemeProvider>
  );
}
```

**Issue**: TypeScript errors with theme

**Solution**: Extend the theme types:
```tsx
import '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Theme {
    custom: {
      myCustomValue: string;
    };
  }
  interface ThemeOptions {
    custom?: {
      myCustomValue?: string;
    };
  }
}
```

**Issue**: Bundle size too large

**Solution**: Use tree-shaking with named imports:
```tsx
// Good - each component imported separately
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

// Avoid - imports entire package
import { Button, TextField } from '@mui/material';
```

**Issue**: Confusion between Grid and Grid2/GridLegacy

**Solution**: In MUI v7:
- Use `import Grid from '@mui/material/Grid'` for current Grid API
- Use `import GridLegacy from '@mui/material/GridLegacy'` for legacy Grid v1
- The `@mui/material/Grid2` import path from v5-v6 has been renamed to Grid
- See [grid-component.md](grid-component.md) for complete Grid documentation

**Issue**: Emotion/styled-components conflict

**Solution**: Choose one styling engine and configure properly:
```bash
# For styled-components
npm install @mui/material @mui/styled-engine-sc styled-components
```

## Migration from v4

Key changes from Material-UI v4 to MUI v5+:

1. **Package name**: `@material-ui/core` → `@mui/material`
2. **Styling engine**: JSS → Emotion (default) or styled-components
3. **Theme structure**: Updated theme API
4. **sx prop**: New styling prop available on all components
5. **Grid component**: New Grid system with simplified API (no `item` prop, new `size` prop)

```bash
# Install codemod tool
npm install -g @mui/codemod

# Run migration
npx @mui/codemod v5.0.0/preset-safe <path>
```

## Community & Resources

**Official Documentation**: [mui.com/material-ui](https://mui.com/material-ui/)

**GitHub**: [github.com/mui/material-ui](https://github.com/mui/material-ui)

**npm**: [@mui/material](https://www.npmjs.com/package/@mui/material)

**Templates**: Pre-built themes and templates available on MUI Store

**Community**: Active Discord, Stack Overflow, and GitHub Discussions

**Complete Component List**: For a comprehensive list of all Material UI components and documentation links, see [llms.txt](llms.txt)

## References

[1]: https://mui.com/material-ui/ "Material-UI Documentation"
[2]: https://mui.com/material-ui/getting-started/ "Material-UI Getting Started"
[3]: https://mui.com/material-ui/customization/theming/ "Material-UI Theming"
[4]: https://mui.com/material-ui/customization/how-to-customize/ "Material-UI Customization"
[5]: https://www.npmjs.com/package/@mui/material "MUI npm Package"
