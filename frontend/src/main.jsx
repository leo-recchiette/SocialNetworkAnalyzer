import React from 'react'
import ReactDOM from 'react-dom/client'
import { MantineProvider, createTheme } from '@mantine/core'
import '@mantine/core/styles.css'
import './styles.css'
import App from './App.jsx'

// Brand palette: 1F1F1F (deep background), 343A40 (surfaces/panels), F8D65B (accent).
const theme = createTheme({
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

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <App />
    </MantineProvider>
  </React.StrictMode>,
)