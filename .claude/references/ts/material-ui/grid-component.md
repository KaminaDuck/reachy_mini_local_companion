---
title: "Material UI Grid Component Reference"
description: "Flexbox-based responsive layout grid component for Material UI v7"
type: "api-reference"
tags: ["mui", "material-ui", "grid", "layout", "flexbox", "responsive", "react", "typescript"]
category: "frontend"
subcategory: "ui-components"
version: "7.x"
last_updated: "2025-11-03"
status: "stable"
sources:
  - name: "Material UI Grid Documentation"
    url: "https://mui.com/material-ui/react-grid/"
  - name: "Material UI Grid API Reference"
    url: "https://mui.com/material-ui/api/grid/"
  - name: "Material UI Grid v2 Migration Guide"
    url: "https://mui.com/material-ui/migration/upgrade-to-grid-v2/"
  - name: "Material UI Grid v2 Blog Post"
    url: "https://mui.com/blog/build-layouts-faster-with-grid-v2/"
related: ["mui-v7.md", "llms.txt"]
author: "unknown"
contributors: []
---

# Material UI Grid Component Reference

The Grid component uses CSS Flexbox (rather than CSS Grid) for high flexibility in creating responsive layouts. ([Material UI Grid Documentation][1]) The Grid is always a flex item, and can be made into a flex container by using the `container` prop. ([Material UI Grid API Reference][2])

## Version Context

**Important**: In Material UI v7 (2025), the Grid component architecture has changed:

- **Current API**: `import Grid from '@mui/material/Grid'` - This is Grid v2, renamed to Grid ([Material UI Grid v2 Migration Guide][3])
- **Legacy API**: `import GridLegacy from '@mui/material/GridLegacy'` - The deprecated Grid v1 component for backward compatibility ([Material UI Grid v2 Migration Guide][3])

The Grid component (formerly Grid2 in v5-v6) features negative margins on all sides by default and a simplified API without the `item` prop. ([Material UI Grid v2 Migration Guide][3])

## Installation

```bash
npm install @mui/material @emotion/react @emotion/styled
```

## Import

```typescript
import Grid from '@mui/material/Grid';
```

For legacy projects:
```typescript
import GridLegacy from '@mui/material/GridLegacy';
```

## Breakpoint System

The Grid component uses five default breakpoints: xs, sm, md, lg, and xl. ([Material UI Grid Documentation][1])

| Breakpoint | Screen Width | Device Type |
|------------|--------------|-------------|
| xs | 0px | Mobile phones |
| sm | 600px | Tablets |
| md | 900px | Small laptops |
| lg | 1200px | Desktops |
| xl | 1536px | Large screens |

You can give integer values for each breakpoint to indicate how many of the 12 available columns are occupied by the component when the viewport width satisfies the breakpoint constraints. ([Material UI Grid Documentation][1])

## Core Props

### container

**Type**: `boolean`
**Default**: `false`

Creates a flex container that wraps grid items. ([Material UI Grid API Reference][2]) This prop is required to enable grid layout functionality. A Grid with the `container` prop uses CSS flexbox to arrange its children. ([Material UI Grid Documentation][1])

```tsx
<Grid container spacing={2}>
  <Grid size={6}>Item 1</Grid>
  <Grid size={6}>Item 2</Grid>
</Grid>
```

### size

**Type**: `number | 'auto' | 'grow' | ResponsiveStyleValue<number | 'auto' | 'grow'>`
**Default**: `undefined`

Defines how many of the 12 columns are occupied. ([Material UI Grid API Reference][2]) This prop replaces the old xs, sm, md, lg, xl props from Grid v1. ([Material UI Grid v2 Migration Guide][3])

**Values**:
- **Number (1-12)**: Fixed column width (e.g., `size={6}` uses 6 of 12 columns)
- **`'auto'`**: Column size automatically adjusts to match content width ([Material UI Grid Documentation][1])
- **`'grow'`**: Equal space distribution among all items with grow ([Material UI Grid Documentation][1])
- **Responsive object**: Different sizes per breakpoint (e.g., `size={{ xs: 12, sm: 6, md: 4 }}`)

```tsx
{/* Fixed size */}
<Grid size={6}>Half width</Grid>

{/* Auto-sized to content */}
<Grid size="auto">Content width</Grid>

{/* Equal distribution */}
<Grid size="grow">Flexible width</Grid>

{/* Responsive sizing */}
<Grid size={{ xs: 12, sm: 6, md: 4 }}>
  Responsive
</Grid>
```

### spacing

**Type**: `number | string | ResponsiveStyleValue<number | string>`
**Default**: `0`

Controls space between children (gap between grid items). ([Material UI Grid API Reference][2]) Can only be used on container components. Uses CSS `gap` property internally. ([Material UI Grid Documentation][1])

```tsx
{/* Fixed spacing */}
<Grid container spacing={2}>
  {/* 16px gap (2 * 8px theme spacing) */}
</Grid>

{/* Responsive spacing */}
<Grid container spacing={{ xs: 2, md: 3 }}>
  {/* 16px on mobile, 24px on desktop */}
</Grid>
```

### columns

**Type**: `number | ResponsiveStyleValue<number>`
**Default**: `12`

Changes the default number of columns. ([Material UI Grid API Reference][2]) This allows you to use a different grid system than the default 12-column layout. ([Material UI Grid Documentation][1])

```tsx
<Grid container columns={{ xs: 4, sm: 8, md: 12 }}>
  <Grid size={{ xs: 2, sm: 4, md: 6 }}>
    {/* Uses half the available columns at each breakpoint */}
  </Grid>
</Grid>
```

### offset

**Type**: `number | 'auto' | ResponsiveStyleValue<number | 'auto'>`
**Default**: `undefined`

Adds space/gaps before a grid item, positioning it further along the row. ([Material UI Grid API Reference][2]) The long-awaited offset feature was added to v2 of the Grid, giving you more flexibility for positioning. ([Material UI Grid v2 Blog Post][4])

```tsx
{/* Offset by 3 columns */}
<Grid size={6} offset={3}>
  Centered with offset
</Grid>

{/* Responsive offset */}
<Grid size={{ xs: 6, md: 2 }} offset={{ xs: 3, md: 0 }}>
  Responsive offset
</Grid>

{/* Auto offset pushes to the right */}
<Grid size={4} offset="auto">
  Pushed right
</Grid>
```

## Spacing Props

### rowSpacing

**Type**: `number | string | ResponsiveStyleValue<number | string>`
**Default**: `spacing` value

Specifies row gap independently. ([Material UI Grid API Reference][2]) Behaves like CSS Grid's `row-gap` property. ([Material UI Grid Documentation][1])

```tsx
<Grid container rowSpacing={2} columnSpacing={1}>
  {/* 16px vertical gap, 8px horizontal gap */}
</Grid>
```

### columnSpacing

**Type**: `number | string | ResponsiveStyleValue<number | string>`
**Default**: `spacing` value

Specifies column gap independently. ([Material UI Grid API Reference][2]) Behaves like CSS Grid's `column-gap` property. ([Material UI Grid Documentation][1])

```tsx
<Grid container
  rowSpacing={1}
  columnSpacing={{ xs: 1, sm: 2, md: 3 }}
>
  {/* Fixed vertical, responsive horizontal spacing */}
</Grid>
```

## Flexbox Alignment Props

### direction

**Type**: `ResponsiveStyleValue<'row' | 'row-reverse'>`
**Default**: `'row'`

Defines flex-direction. ([Material UI Grid API Reference][2]) Note: `column` and `column-reverse` are not supported, as Grid is designed for column-based layouts. ([Material UI Grid Documentation][1])

```tsx
<Grid container direction="row-reverse">
  {/* Items flow right to left */}
</Grid>
```

### alignItems

**Type**: `ResponsiveStyleValue<'flex-start' | 'center' | 'flex-end' | 'stretch' | 'baseline'>`
**Default**: `'stretch'`

Controls vertical alignment of items within the container. ([Material UI Grid API Reference][2])

```tsx
<Grid container alignItems="center">
  {/* Vertically center all items */}
</Grid>
```

### justifyContent

**Type**: `ResponsiveStyleValue<'flex-start' | 'center' | 'flex-end' | 'space-between' | 'space-around' | 'space-evenly'>`
**Default**: `'flex-start'`

Controls horizontal alignment and distribution of items. ([Material UI Grid API Reference][2])

```tsx
<Grid container justifyContent="space-between">
  {/* Distribute items with space between */}
</Grid>
```

### wrap

**Type**: `'nowrap' | 'wrap' | 'wrap-reverse'`
**Default**: `'wrap'`

Defines `flex-wrap` style property. ([Material UI Grid API Reference][2])

```tsx
<Grid container wrap="nowrap">
  {/* Items won't wrap to next line */}
</Grid>
```

## Special Props

### disableEqualOverflow

**Type**: `boolean`
**Default**: `false`

Disables horizontal scrollbars on small viewports by removing negative margins from bottom and right sides. ([Material UI Grid API Reference][2]) A new prop called disableEqualOverflow solves the problem of an unwanted scrollbar appearing on small viewports. ([Material UI Grid v2 Blog Post][4])

**Caveat**: Avoid borders or backgrounds on the Grid when this prop is true, as negative margins only on top/left sides cause visual misalignment. ([Material UI Grid v2 Blog Post][4])

```tsx
<Grid container spacing={3} disableEqualOverflow>
  {/* No unwanted horizontal scrollbar */}
</Grid>
```

### sx

**Type**: `SxProps<Theme>`

The Grid component supports all system properties as props. ([Material UI Grid API Reference][2]) Use the `sx` prop for additional styling with theme-aware values.

```tsx
<Grid
  size={6}
  sx={{
    bgcolor: 'primary.main',
    p: 2,
    borderRadius: 1
  }}
>
  Styled grid item
</Grid>
```

### component

**Type**: `React.ElementType`
**Default**: `'div'`

Override the default root element. ([Material UI Grid API Reference][2])

```tsx
<Grid component="section" container>
  {/* Renders as <section> instead of <div> */}
</Grid>
```

## TypeScript Types

```typescript
// ResponsiveStyleValue allows single value or breakpoint object
type ResponsiveStyleValue<T> =
  | T
  | Array<T | null>
  | { [key in Breakpoint]?: T | null };

type GridDirection = 'row' | 'row-reverse';
type GridSpacing = number | string;
type GridWrap = 'nowrap' | 'wrap' | 'wrap-reverse';
type GridSize = 'auto' | 'grow' | number;
type Breakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

// Main props interface
interface GridProps<D extends React.ElementType = 'div'> {
  container?: boolean;
  size?: GridSize | ResponsiveStyleValue<GridSize>;
  spacing?: GridSpacing | ResponsiveStyleValue<GridSpacing>;
  columns?: number | ResponsiveStyleValue<number>;
  offset?: GridSize | ResponsiveStyleValue<GridSize>;
  rowSpacing?: GridSpacing | ResponsiveStyleValue<GridSpacing>;
  columnSpacing?: GridSpacing | ResponsiveStyleValue<GridSpacing>;
  direction?: ResponsiveStyleValue<GridDirection>;
  alignItems?: ResponsiveStyleValue<string>;
  justifyContent?: ResponsiveStyleValue<string>;
  wrap?: GridWrap;
  disableEqualOverflow?: boolean;
  sx?: SxProps<Theme>;
  component?: React.ElementType;
  // ... plus all system props and native component props
}
```

## Usage Examples

### Basic Fluid Grid

```tsx
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

function BasicGrid() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid size={6}>
          <div>xs=6</div>
        </Grid>
        <Grid size={6}>
          <div>xs=6</div>
        </Grid>
        <Grid size={8}>
          <div>xs=8</div>
        </Grid>
        <Grid size={4}>
          <div>xs=4</div>
        </Grid>
      </Grid>
    </Box>
  );
}
```

### Responsive Layout

```tsx
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

function ResponsiveGrid() {
  return (
    <Grid
      container
      spacing={{ xs: 2, md: 3 }}
      columns={{ xs: 4, sm: 8, md: 12 }}
    >
      {Array.from(Array(6)).map((_, index) => (
        <Grid key={index} size={{ xs: 2, sm: 4, md: 4 }}>
          <Paper sx={{ p: 2 }}>Item {index + 1}</Paper>
        </Grid>
      ))}
    </Grid>
  );
}
```

### Row and Column Spacing

```tsx
function SpacingGrid() {
  return (
    <Grid
      container
      rowSpacing={1}
      columnSpacing={{ xs: 1, sm: 2, md: 3 }}
    >
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Item 1</Paper>
      </Grid>
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Item 2</Paper>
      </Grid>
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Item 3</Paper>
      </Grid>
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Item 4</Paper>
      </Grid>
    </Grid>
  );
}
```

### Using Offset

The offset feature provides flexible positioning options. ([Material UI Grid v2 Blog Post][4])

```tsx
function OffsetGrid() {
  return (
    <Grid container spacing={3} sx={{ flexGrow: 1 }}>
      {/* Centered with offset on mobile */}
      <Grid size={{ xs: 6, md: 2 }} offset={{ xs: 3, md: 0 }}>
        <Paper sx={{ p: 2 }}>Item 1</Paper>
      </Grid>

      {/* Auto offset pushes to the right */}
      <Grid size={{ xs: 4, md: 2 }} offset={{ md: 'auto' }}>
        <Paper sx={{ p: 2 }}>Item 2</Paper>
      </Grid>

      {/* Different offsets per breakpoint */}
      <Grid size={{ xs: 4, md: 2 }} offset={{ xs: 4, md: 0 }}>
        <Paper sx={{ p: 2 }}>Item 3</Paper>
      </Grid>

      {/* Grow with offset */}
      <Grid size={{ xs: 'grow', md: 6 }} offset={{ md: 2 }}>
        <Paper sx={{ p: 2 }}>Item 4</Paper>
      </Grid>
    </Grid>
  );
}
```

### Auto and Grow Sizing

```tsx
function FlexibleGrid() {
  return (
    <Grid container spacing={3}>
      {/* Equal distribution with grow */}
      <Grid size="grow">
        <Paper sx={{ p: 2 }}>Grows to fill space</Paper>
      </Grid>

      {/* Fixed size */}
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Fixed 6 columns</Paper>
      </Grid>

      {/* Auto-sized to content */}
      <Grid size="auto">
        <Paper sx={{ p: 2 }}>Content width</Paper>
      </Grid>
    </Grid>
  );
}
```

### Sidebar Layout with Alignment

```tsx
function SidebarLayout() {
  return (
    <Grid
      container
      spacing={2}
      alignItems="center"
      justifyContent="space-between"
    >
      <Grid size={3}>
        <Paper sx={{ p: 2, height: '100%' }}>
          Sidebar Navigation
        </Paper>
      </Grid>
      <Grid size={9}>
        <Paper sx={{ p: 2 }}>
          Main Content Area
        </Paper>
      </Grid>
    </Grid>
  );
}
```

### Nested Grids

Grid v2 fully supports nested grid structures. ([Material UI Grid v2 Blog Post][4])

```tsx
function NestedGrid() {
  return (
    <Grid container spacing={2}>
      <Grid size={12}>
        <Paper sx={{ p: 2 }}>
          <Grid container spacing={1}>
            <Grid size={6}>Nested 1</Grid>
            <Grid size={6}>Nested 2</Grid>
          </Grid>
        </Paper>
      </Grid>
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Regular Item</Paper>
      </Grid>
      <Grid size={6}>
        <Paper sx={{ p: 2 }}>Regular Item</Paper>
      </Grid>
    </Grid>
  );
}
```

### Complex Dashboard Layout

```tsx
function DashboardLayout() {
  return (
    <Grid container spacing={3}>
      {/* Header spanning full width */}
      <Grid size={12}>
        <Paper sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
          Dashboard Header
        </Paper>
      </Grid>

      {/* Main content area - responsive */}
      <Grid size={{ xs: 12, md: 8 }}>
        <Paper sx={{ p: 2, minHeight: 400 }}>
          Main Content
        </Paper>
      </Grid>

      {/* Sidebar - full width on mobile, 1/3 on desktop */}
      <Grid size={{ xs: 12, md: 4 }}>
        <Grid container spacing={2}>
          <Grid size={12}>
            <Paper sx={{ p: 2 }}>Widget 1</Paper>
          </Grid>
          <Grid size={12}>
            <Paper sx={{ p: 2 }}>Widget 2</Paper>
          </Grid>
        </Grid>
      </Grid>

      {/* Footer cards - responsive grid */}
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <Paper sx={{ p: 2 }}>Card 1</Paper>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <Paper sx={{ p: 2 }}>Card 2</Paper>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <Paper sx={{ p: 2 }}>Card 3</Paper>
      </Grid>
      <Grid size={{ xs: 12, sm: 6, md: 3 }}>
        <Paper sx={{ p: 2 }}>Card 4</Paper>
      </Grid>
    </Grid>
  );
}
```

## Migration from GridLegacy (Grid v1)

### Key Changes

In v2, Grid is always an item—similar to the Flexbox item in CSS—so the item prop is no longer needed. ([Material UI Grid v2 Migration Guide][3])

**Breaking Changes**:
1. **No `item` prop**: Grid is always a flex item by default ([Material UI Grid v2 Migration Guide][3])
2. **New `size` prop**: Replaces individual `xs`, `sm`, `md`, `lg`, `xl` props ([Material UI Grid v2 Migration Guide][3])
3. **Offset feature added**: New positioning capability not in v1 ([Material UI Grid v2 Blog Post][4])
4. **Negative margins on all sides**: Grid2 features negative margins on all sides by default ([Material UI Grid v2 Migration Guide][3])

### Migration Steps

Run the automated codemod:

```bash
npx @mui/codemod v7.0.0/grid-props <path/to/folder>
```

### Before and After Examples

**Grid v1 (GridLegacy)**:
```tsx
<Grid container spacing={2}>
  <Grid item xs={12} sm={6} md={4}>
    <Paper>Item 1</Paper>
  </Grid>
  <Grid item xs={12} sm={6} md={4}>
    <Paper>Item 2</Paper>
  </Grid>
</Grid>
```

**Grid v2 (Current Grid)**:
```tsx
<Grid container spacing={2}>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Paper>Item 1</Paper>
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Paper>Item 2</Paper>
  </Grid>
</Grid>
```

### Handling disableEqualOverflow

If you experience unwanted scrollbars after migrating, use the `disableEqualOverflow` prop:

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  components: {
    MuiGrid: {
      defaultProps: {
        disableEqualOverflow: true,
      },
    },
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

## Best Practices

### 1. Use Responsive Objects for Breakpoints

Prefer responsive objects over single values for flexible layouts:

```tsx
// Good
<Grid size={{ xs: 12, sm: 6, md: 4 }}>
  Content
</Grid>

// Less flexible
<Grid size={6}>
  Content
</Grid>
```

### 2. Always Specify container Prop

Explicitly mark container Grids to make the structure clear:

```tsx
// Good
<Grid container spacing={2}>
  <Grid size={6}>Item</Grid>
</Grid>

// Unclear
<Grid spacing={2}>
  <Grid size={6}>Item</Grid>
</Grid>
```

### 3. Use offset Instead of Empty Items

The offset feature provides cleaner positioning than empty grid items. ([Material UI Grid v2 Blog Post][4])

```tsx
// Good
<Grid size={6} offset={3}>
  Centered content
</Grid>

// Avoid
<Grid size={3} />
<Grid size={6}>
  Centered content
</Grid>
<Grid size={3} />
```

### 4. Leverage grow and auto for Flexible Layouts

Use special size values for dynamic layouts:

```tsx
<Grid container spacing={2}>
  {/* Takes content width */}
  <Grid size="auto">
    <Button>Action</Button>
  </Grid>

  {/* Fills remaining space */}
  <Grid size="grow">
    <Typography>Title</Typography>
  </Grid>

  {/* Takes content width */}
  <Grid size="auto">
    <IconButton><CloseIcon /></IconButton>
  </Grid>
</Grid>
```

### 5. Use rowSpacing and columnSpacing for Independent Control

```tsx
// Better control than single spacing prop
<Grid
  container
  rowSpacing={2}
  columnSpacing={{ xs: 1, sm: 2, md: 3 }}
>
  {/* Items */}
</Grid>
```

### 6. Combine with sx Prop for Additional Styling

```tsx
<Grid
  size={{ xs: 12, md: 6 }}
  sx={{
    bgcolor: 'background.paper',
    p: 2,
    borderRadius: 1,
    boxShadow: 1
  }}
>
  Styled grid item
</Grid>
```

### 7. Remember: Grid Uses Flexbox, Not CSS Grid

- Direction `column` and `column-reverse` are not supported
- Automatic wrapping behavior with `wrap` prop
- Use flex-based alignment props (`alignItems`, `justifyContent`)
- The Grid uses Flexbox internally for layout control ([Material UI Grid Documentation][1])

## Common Patterns

### Equal Height Cards

```tsx
<Grid container spacing={2} alignItems="stretch">
  {items.map((item) => (
    <Grid key={item.id} size={{ xs: 12, sm: 6, md: 4 }}>
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ flexGrow: 1 }}>
          {item.content}
        </CardContent>
      </Card>
    </Grid>
  ))}
</Grid>
```

### Centered Content

```tsx
<Grid
  container
  justifyContent="center"
  alignItems="center"
  sx={{ minHeight: '100vh' }}
>
  <Grid size={{ xs: 11, sm: 8, md: 6, lg: 4 }}>
    <Paper sx={{ p: 4 }}>
      Centered content
    </Paper>
  </Grid>
</Grid>
```

### Responsive Navigation Bar

```tsx
<Grid container spacing={2} alignItems="center">
  <Grid size="auto">
    <Logo />
  </Grid>
  <Grid size="grow">
    <Typography variant="h6">App Title</Typography>
  </Grid>
  <Grid size="auto">
    <Stack direction="row" spacing={1}>
      <Button>Home</Button>
      <Button>About</Button>
      <Button>Contact</Button>
    </Stack>
  </Grid>
</Grid>
```

### Masonry-like Layout

```tsx
<Grid container spacing={2}>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Paper sx={{ p: 2, height: 200 }}>Short</Paper>
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Paper sx={{ p: 2, height: 300 }}>Medium</Paper>
  </Grid>
  <Grid size={{ xs: 12, sm: 6, md: 4 }}>
    <Paper sx={{ p: 2, height: 250 }}>Varied</Paper>
  </Grid>
</Grid>
```

## Performance Considerations

1. **Avoid inline objects**: Define responsive objects outside render for better performance

```tsx
// Good - defined once
const gridSize = { xs: 12, sm: 6, md: 4 };

function MyComponent() {
  return <Grid size={gridSize}>Content</Grid>;
}

// Avoid - recreated on each render
function MyComponent() {
  return <Grid size={{ xs: 12, sm: 6, md: 4 }}>Content</Grid>;
}
```

2. **Use disableEqualOverflow judiciously**: Only enable when necessary for scrollbar issues

3. **Leverage CSS gap**: The Grid uses native CSS `gap` for spacing, which is performant ([Material UI Grid Documentation][1])

## Accessibility

The Grid component uses semantic `<div>` elements by default. ([Material UI Grid API Reference][2]) Enhance accessibility by:

1. **Using semantic HTML**: Override with `component` prop when appropriate

```tsx
<Grid component="nav" container>
  <Grid component="ul" size={12}>
    {/* Navigation items */}
  </Grid>
</Grid>
```

2. **Providing ARIA labels**: Add labels for screen readers

```tsx
<Grid container aria-label="Product grid">
  {/* Items */}
</Grid>
```

3. **Ensuring keyboard navigation**: Grid items should be keyboard accessible

4. **Maintaining focus order**: Grid wrapping preserves logical focus order

## Troubleshooting

### Unwanted Horizontal Scrollbar

Use `disableEqualOverflow` to remove scrollbars on small viewports:

```tsx
<Grid container spacing={2} disableEqualOverflow>
  {/* Content */}
</Grid>
```

### Items Not Wrapping

Check that `wrap` prop is set correctly (default is `'wrap'`):

```tsx
<Grid container wrap="wrap">
  {/* Items will wrap */}
</Grid>
```

### Spacing Not Applied

Ensure `spacing` is used on a Grid with `container` prop:

```tsx
// Correct
<Grid container spacing={2}>
  <Grid size={6}>Item</Grid>
</Grid>

// Incorrect - spacing ignored
<Grid spacing={2}>
  <Grid size={6}>Item</Grid>
</Grid>
```

### Unequal Heights

Use `alignItems="stretch"` and ensure children have `height: 100%`:

```tsx
<Grid container spacing={2} alignItems="stretch">
  <Grid size={6}>
    <Paper sx={{ height: '100%' }}>Equal height</Paper>
  </Grid>
  <Grid size={6}>
    <Paper sx={{ height: '100%' }}>Equal height</Paper>
  </Grid>
</Grid>
```

### Offset Not Working

Verify you're using the correct responsive syntax:

```tsx
// Correct
<Grid size={6} offset={{ xs: 3, md: 0 }}>
  Content
</Grid>

// Incorrect - offset is not an array
<Grid size={6} offset={[3, 0]}>
  Content
</Grid>
```

## Related Components

- **Box**: Generic container with system props, useful for wrapping Grid containers
- **Container**: Centers content horizontally with max-width constraints
- **Stack**: One-dimensional layout (vertical or horizontal), simpler than Grid for single-direction layouts
- **GridLegacy**: Deprecated Grid v1 component for backward compatibility

## References

[1]: https://mui.com/material-ui/react-grid/ "Material UI Grid Documentation"
[2]: https://mui.com/material-ui/api/grid/ "Material UI Grid API Reference"
[3]: https://mui.com/material-ui/migration/upgrade-to-grid-v2/ "Material UI Grid v2 Migration Guide"
[4]: https://mui.com/blog/build-layouts-faster-with-grid-v2/ "Material UI Grid v2 Blog Post"
