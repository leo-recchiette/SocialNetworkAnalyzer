import {
  Badge, Button, Collapse, Divider, Grid, Group, Paper, RangeSlider,
  Select, Slider, Stack, Text, TextInput, Tooltip, UnstyledButton,
} from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { epochToDateLabel } from '../utils.js'

const DAY = 86400

const icon = (name, size = 16, extra = {}) =>
  <i className="material-icons" style={{ fontSize: size, ...extra }}>{name}</i>

// A numeric/text value chip — mono face, matching the brand's "mono for data".
const ValueChip = ({ children }) => (
  <Badge variant="default" radius={0} size="sm"
    styles={{ label: { fontFamily: 'var(--mantine-font-family-monospace)', fontWeight: 600, textTransform: 'none' } }}>
    {children}
  </Badge>
)

// Header row for a slider: label + info tooltip on the left, current value on the right.
const FieldLabel = ({ label, info, children }) => (
  <Group justify="space-between" wrap="nowrap" mb={6}>
    <Group gap={6} wrap="nowrap">
      <Text size="sm" fw={600}>{label}</Text>
      <Tooltip label={info} multiline w={280} withArrow>
        {icon('info', 14, { cursor: 'help', opacity: 0.55 })}
      </Tooltip>
    </Group>
    {children}
  </Group>
)

// Collapsible filter panel: node/edge sliders, the dual-handle date RangeSlider,
// keyword/person search and the social network selector.
export default function FiltersMenu({
  sn, onSnChange,
  keyword, onKeywordChange, person, onPersonChange,
  nodeVal, nodeMax, onNodeChange, onNodeChangeEnd,
  edgeVal, edgeMax, onEdgeChange, onEdgeChangeEnd,
  dateBounds, dateRange, onDateChange, onDateChangeEnd,
  onSearch, searchBtn,
}) {
  const [opened, { toggle }] = useDisclosure(false)

  const nodeInfo = sn === 'mbox'
    ? 'Node value is the sum of all connected edges weight'
    : "Node value rappresents how many times a specific person was tagged by the dump's owner"
  const edgeInfo = sn === 'mbox'
    ? 'Edge value equals the number of emails between two nodes'
    : "Edge value rappresents how many times two people are tagged together by the dump's owner"

  return (
    <Paper withBorder radius={0} mb="sm">
      <UnstyledButton className="sna-menu-toggle" onClick={toggle} w="100%" px="md" py={10}>
        <Group justify="space-between">
          <Group gap={8} wrap="nowrap">
            {icon('tune', 18, { color: 'var(--mantine-primary-color-filled)' })}
            <Text fw={600}>Menu</Text>
          </Group>
          {icon('expand_more', 22, {
            transition: 'transform 150ms ease',
            transform: opened ? 'rotate(180deg)' : 'none',
            opacity: 0.7,
          })}
        </Group>
      </UnstyledButton>

      <Collapse in={opened}>
        <Divider />
        <Grid p="md" gutter="lg">
          <Grid.Col span={{ base: 12, lg: 8 }}>
            <Grid gutter="lg">
              <Grid.Col span={{ base: 12, sm: 6 }}>
                <FieldLabel label="Min Node Value" info={nodeInfo}>
                  <ValueChip>{nodeVal}</ValueChip>
                </FieldLabel>
                <Slider min={0} max={nodeMax} value={nodeVal} thumbSize={16}
                  onChange={onNodeChange} onChangeEnd={onNodeChangeEnd} size="sm" />
              </Grid.Col>
              <Grid.Col span={{ base: 12, sm: 6 }}>
                <FieldLabel label="Min Edges Value" info={edgeInfo}>
                  <ValueChip>{edgeVal}</ValueChip>
                </FieldLabel>
                <Slider min={0} max={edgeMax} value={edgeVal} thumbSize={16}
                  onChange={onEdgeChange} onChangeEnd={onEdgeChangeEnd} size="sm" />
              </Grid.Col>
            </Grid>

            <Stack gap={6} mt="lg">
              <FieldLabel label="Date range">
                <ValueChip>{epochToDateLabel(dateRange[0])} → {epochToDateLabel(dateRange[1])}</ValueChip>
              </FieldLabel>
              <RangeSlider
                min={dateBounds[0]}
                max={dateBounds[1]}
                step={DAY}
                minRange={DAY}
                value={dateRange}
                onChange={onDateChange}
                onChangeEnd={onDateChangeEnd}
                label={epochToDateLabel}
                thumbSize={16}
                size="sm"
              />
            </Stack>
          </Grid.Col>

          <Grid.Col span={{ base: 12, lg: 4 }}>
            <Grid>
              <Grid.Col span={6}>
                <Stack gap="sm">
                  <TextInput
                    placeholder="Search a keyword"
                    leftSection={icon('edit')}
                    value={keyword}
                    onChange={(e) => onKeywordChange(e.currentTarget.value)}
                  />
                  <TextInput
                    placeholder="Search a name"
                    leftSection={icon('person')}
                    value={person}
                    onChange={(e) => onPersonChange(e.currentTarget.value)}
                  />
                </Stack>
              </Grid.Col>
              <Grid.Col span={6}>
                <Stack gap="sm">
                  <Select
                    leftSection={icon('people')}
                    data={[
                      { value: 'facebook', label: 'Facebook' },
                      { value: 'twitter', label: 'Twitter' },
                      { value: 'mbox', label: 'Mail box' },
                    ]}
                    value={sn}
                    onChange={(v) => v && onSnChange(v)}
                    allowDeselect={false}
                  />
                  <Button fullWidth color={searchBtn.color} onClick={onSearch}
                    leftSection={icon('search')}>
                    {searchBtn.label}
                  </Button>
                </Stack>
              </Grid.Col>
            </Grid>
          </Grid.Col>
        </Grid>
      </Collapse>
    </Paper>
  )
}
