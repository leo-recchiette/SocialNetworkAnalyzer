import { createTheme } from '@mantine/core'

// Brand palette: 1F1F1F (deep background), 343A40 (surfaces/panels), F8D65B (accent).
// Shared by the app root (main.jsx) and the standalone React roots the legacy
// modules mount into the imperative .data/.content islands (e.g. the word
// frequency panel), so every Mantine surface renders with the same brand.
export const theme = createTheme({
  primaryColor: 'yellow',
  primaryShade: 4,
  defaultRadius: 0,
  // dark text on yellow fills instead of white
  autoContrast: true,
  colors: {
    // dark[7] = body background (1F1F1F), dark[6] = surfaces (343A40),
    // dark[4]/[5] = borders/hover; lighter indices stay neutral for text.
    dark: [
      '#c9c9c9', '#b8b8b8', '#9a9ea3', '#6c727a', '#454c54',
      '#3c424a', '#343A40', '#1F1F1F', '#191919', '#121212',
    ],
    // yellow[4] = F8D65B (primaryShade), with lighter/darker steps around it.
    yellow: [
      '#fff9e3', '#fdf1c4', '#fbe79a', '#f9de71', '#f8d65b',
      '#e6c044', '#cda730', '#a07f22', '#735b16', '#46370a',
    ],
  },
})
