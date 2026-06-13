import {
  Button, Collapse, Grid, Group, Paper, RangeSlider, Select, Slider, Text, TextInput, Tooltip, UnstyledButton,
} from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { epochToDateLabel } from '../utils.js'

const DAY = 86400

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
      <UnstyledButton onClick={toggle} w="100%" px="md" py={6}>
        <Group justify="space-between">
          <Text fw={500}>Menu</Text>
          <i className="material-icons">{opened ? 'keyboard_arrow_up' : 'keyboard_arrow_down'}</i>
        </Group>
      </UnstyledButton>

      <Collapse in={opened}>
        <Grid p="md" pt={0}>
          <Grid.Col span={{ base: 12, lg: 8 }}>
            <Grid>
              <Grid.Col span={{ base: 12, lg: 6 }}>
                <Group gap={6}>
                  <Text size="sm" fw={700}>Min Node Value:</Text>
                  <Text size="sm">{nodeVal}</Text>
                  <Tooltip label={nodeInfo} multiline w={280}>
                    <i className="material-icons" style={{ fontSize: 14, cursor: 'help' }}>info</i>
                  </Tooltip>
                </Group>
                <Slider min={0} max={nodeMax} value={nodeVal}
                  onChange={onNodeChange} onChangeEnd={onNodeChangeEnd} size="sm" />
              </Grid.Col>
              <Grid.Col span={{ base: 12, lg: 6 }}>
                <Group gap={6}>
                  <Text size="sm" fw={700}>Min Edges Value:</Text>
                  <Text size="sm">{edgeVal}</Text>
                  <Tooltip label={edgeInfo} multiline w={280}>
                    <i className="material-icons" style={{ fontSize: 14, cursor: 'help' }}>info</i>
                  </Tooltip>
                </Group>
                <Slider min={0} max={edgeMax} value={edgeVal}
                  onChange={onEdgeChange} onChangeEnd={onEdgeChangeEnd} size="sm" />
              </Grid.Col>
            </Grid>

            <Group gap={6} mt="md">
              <Text size="sm" fw={700}>Date range:</Text>
              <Text size="sm">{epochToDateLabel(dateRange[0])} - {epochToDateLabel(dateRange[1])}</Text>
            </Group>
            <RangeSlider
              min={dateBounds[0]}
              max={dateBounds[1]}
              step={DAY}
              minRange={DAY}
              value={dateRange}
              onChange={onDateChange}
              onChangeEnd={onDateChangeEnd}
              label={epochToDateLabel}
              size="sm"
            />
          </Grid.Col>

          <Grid.Col span={{ base: 12, lg: 2 }}>
            <TextInput
              placeholder="Search a keyword"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>edit</i>}
              value={keyword}
              onChange={(e) => onKeywordChange(e.currentTarget.value)}
              mb="sm"
              size="sm"
            />
            <TextInput
              placeholder="Search a name"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>person</i>}
              value={person}
              onChange={(e) => onPersonChange(e.currentTarget.value)}
              size="sm"
            />
          </Grid.Col>

          <Grid.Col span={{ base: 12, lg: 2 }}>
            <Select
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>people</i>}
              data={[
                { value: 'facebook', label: 'Facebook' },
                { value: 'twitter', label: 'Twitter' },
                { value: 'mbox', label: 'Mail box' },
              ]}
              value={sn}
              onChange={(v) => v && onSnChange(v)}
              allowDeselect={false}
              mb="sm"
              size="sm"
            />
            <Button fullWidth color={searchBtn.color} onClick={onSearch}>{searchBtn.label}</Button>
          </Grid.Col>
        </Grid>
      </Collapse>
    </Paper>
  )
}