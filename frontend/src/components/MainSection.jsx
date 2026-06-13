import { ActionIcon, Group, Paper, Radio, SegmentedControl, Select, Text, Tooltip } from '@mantine/core'

const GRAPH_INFO = {
  relNet: "The relathionship graph shows how the people are added and tagged by dump's owner in a selected range of time. " +
    'The node size depends on how many times a person is tagged. The bigger the node is, more times the person is tagged. ' +
    'The link between two people depends on how many times they are tagged together. The bigger the link is, more times they are tagged together.',
  trafficNet: "The message traffic network shows the contents shared by dump's owner in a selected range of time. " +
    'The node size depends on how many people are tagged in. The bigger the node is, more people are tagged in it.',
  map: 'The map shows the content shared in a specific geo location.',
  wordFrec: 'The word frequency shows the most frequently used words in the selected time range. ' +
    'Warning: This option may take a long time in case of very large content. Use with caution.',
}

function graphLabel(text, info) {
  return (
    <Group gap={4} wrap="nowrap" justify="center">
      <span>{text}</span>
      <Tooltip label={info} multiline w={320}>
        <i className="material-icons" style={{ fontSize: 13 }}>info</i>
      </Tooltip>
    </Group>
  )
}

function RadioRow({ value, onChange, options }) {
  return (
    <Radio.Group value={value} onChange={onChange}>
      <Group gap="md" wrap="nowrap">
        {options.map((o) => (
          <Radio key={o.value} size="xs" value={o.value} label={o.label}
            styles={{ label: { color: '#18181b' } }} />
        ))}
      </Group>
    </Radio.Group>
  )
}

// Central area: graph canvas (.content, owned by the legacy modules) with the
// per-graph filter radios floating on top, the graph-type selector below, and
// the data panel (.data) with its tabs on the right.
export default function MainSection({
  active, sn, graphType, onGraphTypeChange,
  fbUserType, onFbUserType, fbNodeType, onFbNodeType, fbMap, onFbMap,
  twUserType, onTwUserType, tweetType, onTweetType, twNodeType, onTwNodeType,
  onStabilize,
  dataViz1, onDataViz1, dataViz2, onDataViz2,
  sortValue, onSortChange,
}) {
  const isNet = graphType === 'relNet' || graphType === 'trafficNet'

  // ported from the old enableDisableButtons()
  const dataViz1Disabled = (v) =>
    graphType === 'trafficNet' && (v === 'filtered' || v === 'all')
  const dataViz2Disabled = (v) =>
    (graphType === 'trafficNet' && v === 'links') ||
    graphType === 'map' || graphType === 'wordFrec'
  const sortDisabled = graphType === 'wordFrec'

  const sortOptions = [
    { value: 'timedesc', label: 'Time descending' },
    { value: 'timeasc', label: 'Time ascending' },
    { value: 'name', label: 'Name' },
    { value: 'tagcount', label: 'Tagged together count' },
    { value: 'degree', label: 'Node degree' },
  ].map((o) => ({
    ...o,
    disabled: dataViz2 === 'links' && o.value !== 'tagcount',
  }))

  // 343A40 surface so the right-column tabs read as a panel over the 1F1F1F body
  // (inactive labels stay light; the active label gets dark text on the yellow
  // indicator via the theme's autoContrast)
  const tabStyles = {
    root: { background: 'var(--mantine-color-dark-6)', borderRadius: 0 },
  }

  return (
    <div style={{ display: 'flex', flex: 1, minHeight: 0, flexDirection: 'column' }}>
      <div style={{ display: 'flex', flex: 1, minHeight: 0, gap: 12 }}>
      {/* left column: graph */}
      <div style={{ flex: 3, minWidth: 0, position: 'relative', display: 'flex', flexDirection: 'column' }}>
        <div style={{ position: 'absolute', top: 4, left: 8, right: 8, zIndex: 30 }}>
          <Group gap="sm" wrap="nowrap">
            {active && isNet && (
              <Tooltip label="Stop dynamic graph">
                <ActionIcon variant="subtle" color="dark" onClick={onStabilize} aria-label="Stop dynamic graph">
                  <i className="material-icons" style={{ fontSize: 18 }}>block</i>
                </ActionIcon>
              </Tooltip>
            )}

            {active && sn === 'facebook' && graphType === 'relNet' && (
              <RadioRow value={fbUserType} onChange={onFbUserType} options={[
                { value: 'Friend', label: 'Friend' },
                { value: 'remFriend', label: 'Removed friend' },
                { value: 'All', label: 'All' },
              ]} />
            )}
            {active && sn === 'facebook' && graphType === 'trafficNet' && (
              <RadioRow value={fbNodeType} onChange={onFbNodeType} options={[
                { value: 'all', label: 'All' },
                { value: 'post', label: 'Posts' },
                { value: 'friendPost', label: 'Friends posts' },
                { value: 'comment', label: 'Comments' },
                { value: 'dm', label: 'Direct messages' },
              ]} />
            )}
            {active && sn === 'facebook' && graphType === 'map' && (
              <RadioRow value={fbMap} onChange={onFbMap} options={[
                { value: 'post', label: 'Post' },
                { value: 'geoTag', label: 'Geo Tag' },
                { value: 'all', label: 'All' },
              ]} />
            )}
            {active && sn === 'twitter' && graphType === 'relNet' && (
              <RadioRow value={twUserType} onChange={onTwUserType} options={[
                { value: 'follower', label: 'Follower' },
                { value: 'following', label: 'Following' },
                { value: 'All', label: 'All' },
              ]} />
            )}
            {active && sn === 'twitter' && graphType === 'trafficNet' && (
              <>
                <RadioRow value={tweetType} onChange={onTweetType} options={[
                  { value: 'all', label: 'All' },
                  { value: 'tweet', label: 'Tweet' },
                  { value: 'retweet', label: 'Retweet' },
                ]} />
                <RadioRow value={twNodeType} onChange={onTwNodeType} options={[
                  { value: 'nodeDegree', label: 'Node degree' },
                  { value: 'retweet_count', label: 'Retweet count' },
                ]} />
              </>
            )}
          </Group>
        </div>

        {/* imperative canvas - rendered into by neovis / openlayers / gantt */}
        <div className="content" style={{ flex: 1, minHeight: 0 }} />
      </div>

      {/* right column: data panel */}
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
        <SegmentedControl
          color="yellow"
          fullWidth
          size="xs"
          value={dataViz1}
          onChange={onDataViz1}
          data={[
            { value: 'selected', label: 'Selected', disabled: dataViz1Disabled('selected') },
            { value: 'filtered', label: 'Filtered', disabled: dataViz1Disabled('filtered') },
            { value: 'all', label: 'All', disabled: dataViz1Disabled('all') },
          ]}
          radius={0}
          styles={tabStyles}
        />
        <SegmentedControl
          color="yellow"
          fullWidth
          size="xs"
          value={dataViz2}
          onChange={onDataViz2}
          data={[
            { value: 'contacts', label: 'Contacts', disabled: dataViz2Disabled('contacts') },
            { value: 'links', label: 'Links', disabled: dataViz2Disabled('links') },
          ]}
          radius={0}
          styles={tabStyles}
        />
        <Paper p={6} radius={0} withBorder>
          <Group gap="xs" wrap="nowrap">
            <Text size="sm" style={{ whiteSpace: 'nowrap' }}>Sort by:</Text>
            <Select
              size="xs"
              style={{ flex: 1 }}
              data={sortOptions}
              value={sortValue}
              onChange={(v) => v && onSortChange(v)}
              allowDeselect={false}
              disabled={sortDisabled}
            />
          </Group>
        </Paper>

        {/* imperative panel - rendered into by dataVisualization.js */}
        <div className="navigation" style={{ flex: 1, minHeight: 0 }}>
          <div className="data" />
        </div>
      </div>
      </div>

      {/* full-width graph-type selector, matching the top Menu box */}
      <SegmentedControl
        color="yellow"
        fullWidth
        mt={12}
        value={graphType}
        onChange={onGraphTypeChange}
        data={[
          { value: 'relNet', label: graphLabel('Relationships network', GRAPH_INFO.relNet) },
          { value: 'trafficNet', label: graphLabel('Messages traffic network', GRAPH_INFO.trafficNet) },
          { value: 'map', label: graphLabel('Map', GRAPH_INFO.map) },
          { value: 'wordFrec', label: graphLabel('Word frequency', GRAPH_INFO.wordFrec) },
        ]}
        radius={0}
        styles={tabStyles}
      />
    </div>
  )
}