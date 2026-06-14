import {
  Accordion, Anchor, Center, Divider, Group, Loader, Stack, Table, Text, ThemeIcon,
} from '@mantine/core'

// Real-Mantine rendering of the .data side panel. dataVisualization.js builds a
// plain-object `model` (see its builders) from the server response and hands it
// here; this module owns all the markup. The panel is a light zinc island, so
// text is dark (#18181b) and counts/IDs/timestamps use a mono face per the
// design system. Rendered into the React-owned panel (DataPanelHost).

const DARK = '#18181b'
const MUTED = '#3f3f46'

function FieldValue({ value, href, mono }) {
  if (href) return <Anchor href={href} target="_blank" size="sm" c="#735b16" underline="always">link</Anchor>
  const v = value == null || value === '' ? '—' : String(value)
  return (
    <Text component="span" size="sm" c={DARK}
      ff={mono ? 'monospace' : undefined} style={{ overflowWrap: 'break-word' }}>
      {v}
    </Text>
  )
}

function Field({ label, value, href, mono }) {
  return (
    <div>
      {label ? <Text component="span" size="sm" fw={700} c={DARK}>{label}: </Text> : null}
      <FieldValue value={value} href={href} mono={mono} />
    </div>
  )
}

function ItemList({ label, items }) {
  return (
    <div>
      <Text component="span" size="sm" fw={700} c={DARK}>{label}: </Text>
      <Stack gap={0} mt={2}>
        {(items || []).map((it, i) => (
          <Text key={i} size="sm" c={DARK} style={{ overflowWrap: 'break-word' }}>{it}</Text>
        ))}
      </Stack>
    </div>
  )
}

// The original markup carried a ".spoiler-btn" with no toggle handler, so the
// tagged-with list was always hidden; an Accordion makes it actually expandable.
function TaggedSpoiler({ label, items }) {
  return (
    <Accordion variant="contained" radius={0} chevronPosition="left"
      styles={{
        item: { backgroundColor: '#f4f4f5', borderColor: '#d4d4d8' },
        control: { padding: '4px 8px' },
        label: { padding: 0, fontSize: '0.75rem', color: MUTED },
        content: { padding: '4px 8px' },
      }}>
      <Accordion.Item value="tagged">
        <Accordion.Control>{label}</Accordion.Control>
        <Accordion.Panel>
          <Stack gap={2}>
            {(items || []).map((it, i) => (
              <Text key={i} size="sm" c={DARK}
                style={{ borderLeft: '4px double #3f3f46', paddingLeft: '0.875rem' }}>
                {it}
              </Text>
            ))}
          </Stack>
        </Accordion.Panel>
      </Accordion.Item>
    </Accordion>
  )
}

function RecordCard({ record }) {
  return (
    <Stack gap={4}>
      {(record.fields || []).map((f, i) => <Field key={i} {...f} />)}
      {(record.lists || []).map((l, i) => <ItemList key={i} {...l} />)}
      {record.spoiler ? <TaggedSpoiler {...record.spoiler} /> : null}
    </Stack>
  )
}

function LinksTable({ rows }) {
  return (
    <Table verticalSpacing={4} fz="sm" withRowBorders={false}
      styles={{ th: { color: DARK }, td: { color: DARK } }}>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Name</Table.Th>
          <Table.Th>Name</Table.Th>
          <Table.Th>Tagged together</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.map((r, i) => (
          <Table.Tr key={i}>
            <Table.Td style={{ wordWrap: 'break-word' }}>{r.name1}</Table.Td>
            <Table.Td style={{ wordWrap: 'break-word' }}>{r.name2}</Table.Td>
            <Table.Td style={{ wordWrap: 'break-word', fontWeight: 700, fontFamily: 'monospace' }}>
              {r.link}
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  )
}

function Words({ title, rows }) {
  return (
    <Stack gap="sm">
      {title ? <Text size="sm" fw={700} c={DARK}>{title}</Text> : null}
      {rows.map((r, i) => (
        <div key={i}>
          {i > 0 ? <Divider color="#3f3f46" mb="sm" /> : null}
          <Field label="Word" value={r.word} />
          <Field label="Value" value={`${r.value}%`} mono />
        </div>
      ))}
    </Stack>
  )
}

// ---- small shared states used by dom.js / the click-handler error paths ----

export function Hint({ text }) {
  return (
    <Center py="lg" px="xs">
      <Group gap="xs" wrap="nowrap" justify="center">
        <ThemeIcon variant="light" color="yellow" radius={0} size="md">
          <i className="material-icons" style={{ fontSize: 18 }}>touch_app</i>
        </ThemeIcon>
        <Text size="sm" c={MUTED} ta="center">{text}</Text>
      </Group>
    </Center>
  )
}

export function Spinner() {
  return <Center py="lg"><Loader color="yellow" size="sm" /></Center>
}

export function NoData() {
  return (
    <Center py="lg" px="xs">
      <Group gap="xs" wrap="nowrap" justify="center">
        <ThemeIcon variant="light" color="red" radius={0} size="md">
          <i className="material-icons" style={{ fontSize: 18 }}>error</i>
        </ThemeIcon>
        <Text size="sm" c="#b91c1c" ta="center">
          There isn’t any data that can satisfy your research
        </Text>
      </Group>
    </Center>
  )
}

// model.kind: 'placeholder' | 'records' | 'links' | 'words'
export function DataPanel({ model }) {
  if (!model) return null
  if (model.kind === 'placeholder') return <Hint text={model.text} />
  if (model.kind === 'links') return <LinksTable rows={model.rows} />
  if (model.kind === 'words') return <Words title={model.title} rows={model.rows} />
  return (
    <Stack gap="sm">
      {model.records.map((r, i) => (
        <div key={i}>
          {i > 0 ? <Divider color="#3f3f46" mb="sm" /> : null}
          <RecordCard record={r} />
        </div>
      ))}
    </Stack>
  )
}
