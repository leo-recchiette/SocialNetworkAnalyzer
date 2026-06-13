import { useRef, useState } from 'react'
import {
  ActionIcon, Button, Divider, Drawer, FileButton, Group,
  Progress, Radio, Stack, Text, Tooltip,
} from '@mantine/core'

// Dump-management drawer (opened from the navbar account menu): upload a new
// dump and delete existing ones. Account settings live in AccountModal.
export default function SideDrawer({ opened, onClose, onUpload, upload, onDeleteDump, deleteFeedback }) {
  const [file, setFile] = useState(null)
  const [wordFrecOption, setWordFrecOption] = useState('false')
  const [socialToDelete, setSocialToDelete] = useState(null)
  const resetRef = useRef(null)

  const dumpRow = (value, label) => (
    <Group key={value} justify="space-between" wrap="nowrap" py={4}>
      <Radio
        size="xs"
        value={value}
        label={deleteFeedback && deleteFeedback.target === value
          ? <Text span c="red" size="sm">{deleteFeedback.msg}</Text>
          : label}
        checked={socialToDelete === value}
        onChange={() => setSocialToDelete(value)}
      />
      <ActionIcon
        variant="subtle"
        color="red"
        aria-label={'delete ' + label}
        onClick={() => { if (socialToDelete === value) onDeleteDump(value) }}
      >
        <i className="material-icons" style={{ fontSize: 18 }}>delete_forever</i>
      </ActionIcon>
    </Group>
  )

  return (
    <Drawer opened={opened} onClose={onClose} title={<b>Manage dumps</b>} padding="md" size={340}>
      <Stack gap="lg">
        <div>
          <Text fw={700} size="sm" mb="xs">Upload dump</Text>
          <Stack gap="sm">
            <Group gap="xs">
              <FileButton resetRef={resetRef} onChange={setFile} accept=".zip,.mbox">
                {(props) => (
                  <Button {...props} variant="default" size="xs"
                    leftSection={<i className="material-icons" style={{ fontSize: 14 }}>publish</i>}>
                    Choose file
                  </Button>
                )}
              </FileButton>
              <Text size="xs" c="dimmed" style={{ wordBreak: 'break-all' }}>
                {file ? file.name : 'zip (facebook/twitter) or mbox'}
              </Text>
            </Group>

            <Radio.Group
              label={
                <Tooltip multiline w={260}
                  label="This option allow to preload the TFIDF value for the words in the dataset. If you choose NO, the word frequency will be load at runtime">
                  <span>Preload word frequency:</span>
                </Tooltip>
              }
              value={wordFrecOption}
              onChange={setWordFrecOption}
            >
              <Group gap="md" mt={4}>
                <Radio size="xs" value="true" label="Yes" />
                <Radio size="xs" value="false" label="No" />
              </Group>
            </Radio.Group>

            {upload.visible && (
              <div>
                {upload.progress !== null && (
                  <Progress value={upload.progress} striped animated size="lg" />
                )}
                {upload.msg && (
                  <Text size="xs" ta="center" c={upload.msgColor} mt={4}>{upload.msg}</Text>
                )}
              </div>
            )}

            <Button fullWidth color={upload.btnColor} size="sm"
              onClick={() => onUpload(file, wordFrecOption)}>
              {upload.btnLabel}
            </Button>
          </Stack>
        </div>

        <Divider />

        <div>
          <Text fw={700} size="sm" mb="xs">Delete your dumps</Text>
          {dumpRow('facebook', 'Facebook')}
          {dumpRow('twitter', 'Twitter')}
          {dumpRow('mbox', 'Mailbox')}
          {dumpRow('all', 'Delete all')}
        </div>
      </Stack>
    </Drawer>
  )
}
