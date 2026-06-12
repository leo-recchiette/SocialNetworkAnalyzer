import React from 'react'
import ReactDOM from 'react-dom/client'
import { MantineProvider, createTheme } from '@mantine/core'
import '@mantine/core/styles.css'
import './styles.css'
import App from './App.jsx'

const theme = createTheme({
  primaryColor: 'yellow',
  defaultRadius: 'md',
  // dark text on yellow fills instead of white
  autoContrast: true,
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <App />
    </MantineProvider>
  </React.StrictMode>,
)