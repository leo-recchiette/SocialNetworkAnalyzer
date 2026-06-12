import { Grid, Modal, Text } from '@mantine/core'

export default function HelpModal({ opened, onClose }) {
  return (
    <Modal opened={opened} onClose={onClose} title={<b>Help</b>} size="xl" centered>
      <Text size="sm" component="div">
        This tool will drive you through a forensic data analysis of yours <b>facebook, twitter and mbox dumps</b>.
        <br />
        If you haven't done it yet, you'll need to upload the social network dump for analysis.
        <br />
        Once you have uploaded the dump and the data has been processed you can interact with the four tabs in the
        main section which correspond to the four ways you can analyze the data.
        <br /><br />
        In the first two panels, different colors of the nodes represent different types of data represented.
        This nodes can be filtered in the menu at the top of the main section of the application.
        <br /><br />
        <Grid>
          <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
            <Text fw={700} ta="center" size="sm">Relationships network</Text>
            <Text size="xs" ta="justify" mt="xs">
              The relathionship graph shows how the people are added and tagged by dump's owner in a selected range
              of time. The node size depends on how many times a person is tagged. The bigger the node is, more
              times the person is tagged. The link between two people depends on how many times they are tagged
              together. The bigger the link is, more times they are tagged together.
            </Text>
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
            <Text fw={700} ta="center" size="sm">Messages traffic network</Text>
            <Text size="xs" ta="justify" mt="xs">
              The message traffic network shows the contents shared by dump's owner in a selected range of time.
              The node size depends on how many people are tagged in. The bigger the node is, more people are
              tagged in it.
            </Text>
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
            <Text fw={700} ta="center" size="sm">Map</Text>
            <Text size="xs" ta="justify" mt="xs">
              The map shows the content shared in a specific geo location in a selected range of time.
            </Text>
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6, lg: 3 }}>
            <Text fw={700} ta="center" size="sm">Word frequency network</Text>
            <Text size="xs" ta="justify" mt="xs">
              The word frequency shows the most relevant used words in the selected time range.<br />
              <Text span c="red" fs="italic" td="underline" fw={700} size="xs">
                Warning: This option may take a long time in case of very large content. Use with caution.
              </Text>
            </Text>
          </Grid.Col>
        </Grid>
        <br />
        The data to visualize could be filtered using the filters in the <b>menu panel</b>; there are a node slider,
        an edge slider and the time range slide. The filtered options are always available, but it is not advisable
        to work on very large time ranges because this means downloading a very large amount of data.
        <br />
        At the right side users have the ability to select what kind of information they want to see using the two
        tabs on the top, according to that decision the system will generate the corresponding information below.
      </Text>
    </Modal>
  )
}