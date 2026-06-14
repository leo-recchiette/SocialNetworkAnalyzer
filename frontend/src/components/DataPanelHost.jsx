import { useEffect, useRef, useState } from 'react'
import { MantineProvider } from '@mantine/core'
import { theme } from '../theme.js'
import { sna } from '../legacy/bridge.js'

// React owner of the .data side panel. The legacy modules (dataVisualization,
// the word-frequency panel, the dom.js helpers) build a React node and push it
// here via sna.setDataPanel(node) instead of writing HTML into .data.
//
// The panel is a light zinc island on the dark shell. This MantineProvider is
// NESTED inside the app's global (dark) provider, so it does NOT manage the
// document color scheme — it only scopes a light scheme locally via
// getRootElement + cssVariablesSelector (both pointing at the .data element).
// A separate React root would be treated as top-level and flip <html> to light.
export default function DataPanelHost() {
  const ref = useRef(null)
  const [content, setContent] = useState(null)

  useEffect(() => {
    sna.setDataPanel = (node) => setContent(node ?? null)
    return () => { sna.setDataPanel = () => {} }
  }, [])

  return (
    <div className="data" ref={ref}>
      <MantineProvider
        theme={theme}
        forceColorScheme="light"
        getRootElement={() => ref.current || undefined}
        cssVariablesSelector=".data"
      >
        {content}
      </MantineProvider>
    </div>
  )
}
