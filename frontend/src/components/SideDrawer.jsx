import { useRef, useState } from 'react'
import {
  Accordion, Button, Divider, Drawer, FileButton, Group, PasswordInput,
  Progress, Radio, Stack, Text, TextInput, Tooltip, ActionIcon,
} from '@mantine/core'

// Left side panel: auth, dump upload, dump deletion, account settings.
export default function SideDrawer({
  opened, onClose, usr,
  onLogin, onRegister, onLogout, onOpenHelp,
  onUpload, upload,
  onDeleteDump, deleteFeedback,
  onChangeMail, onChangePassword, changeMailBtn, changePassBtn,
  loginFeedback, registerBtn,
}) {
  const [mail, setMail] = useState('')
  const [password, setPassword] = useState('')
  const [file, setFile] = useState(null)
  const [wordFrecOption, setWordFrecOption] = useState('false')
  const [socialToDelete, setSocialToDelete] = useState(null)
  const [newMail, setNewMail] = useState('')
  const [newMailRe, setNewMailRe] = useState('')
  const [newPass, setNewPass] = useState('')
  const [newPassRe, setNewPassRe] = useState('')
  const resetRef = useRef(null)

  const logged = usr !== ''

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
    <Drawer opened={opened} onClose={onClose} title="Profile settings" padding="md" size={320}>
      <Stack justify="space-between" mih="calc(100vh - 80px)">
        <div>
          {!logged && (
            <Stack gap="sm">
              <TextInput
                placeholder="Insert email"
                leftSection={<i className="material-icons" style={{ fontSize: 16 }}>mail</i>}
                value={mail}
                onChange={(e) => setMail(e.currentTarget.value)}
                error={loginFeedback.field === 'mail' ? loginFeedback.msg : null}
              />
              <PasswordInput
                placeholder="Insert password"
                autoComplete="new-password"
                leftSection={<i className="material-icons" style={{ fontSize: 16 }}>vpn_key</i>}
                value={password}
                onChange={(e) => setPassword(e.currentTarget.value)}
                error={loginFeedback.field === 'password' ? loginFeedback.msg : null}
              />
              <Button fullWidth onClick={() => onLogin(mail, password)}>Login</Button>
              <Divider label="or" labelPosition="center" />
              <Tooltip label="Insert a valid email and a valid password, then click register" position="bottom" withArrow>
                <Button fullWidth variant="outline" color={registerBtn.color} onClick={() => onRegister(mail, password)}>
                  {registerBtn.label}
                </Button>
              </Tooltip>
            </Stack>
          )}

          {logged && (
            <>
              <Text size="sm" ta="center" mb="sm">
                You are logged as <b>{usr}</b>
              </Text>
              <Divider mb="sm" />

              <Accordion variant="separated" multiple>
                <Accordion.Item value="upload">
                  <Accordion.Control>Upload dump</Accordion.Control>
                  <Accordion.Panel>
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
                  </Accordion.Panel>
                </Accordion.Item>

                <Accordion.Item value="delete">
                  <Accordion.Control>Delete your dumps</Accordion.Control>
                  <Accordion.Panel>
                    {dumpRow('facebook', 'Facebook')}
                    {dumpRow('twitter', 'Twitter')}
                    {dumpRow('mbox', 'Mailbox')}
                    {dumpRow('all', 'Delete all')}
                  </Accordion.Panel>
                </Accordion.Item>

                <Accordion.Item value="settings">
                  <Accordion.Control>Settings</Accordion.Control>
                  <Accordion.Panel>
                    <Text size="sm" fw={500} mb={4}>Change your email</Text>
                    <Stack gap="xs" mb="md">
                      <TextInput size="xs" placeholder="Insert new email" value={newMail}
                        onChange={(e) => setNewMail(e.currentTarget.value)} />
                      <TextInput size="xs" placeholder="Retype new email" value={newMailRe}
                        onChange={(e) => setNewMailRe(e.currentTarget.value)} />
                      <Button size="xs" variant="outline" color={changeMailBtn.color}
                        onClick={() => onChangeMail(newMail, newMailRe)}>
                        {changeMailBtn.label}
                      </Button>
                    </Stack>

                    <Text size="sm" fw={500} mb={4}>Change your password</Text>
                    <Stack gap="xs">
                      <PasswordInput size="xs" placeholder="Insert new password" value={newPass}
                        onChange={(e) => setNewPass(e.currentTarget.value)} />
                      <PasswordInput size="xs" placeholder="Retype new password" value={newPassRe}
                        onChange={(e) => setNewPassRe(e.currentTarget.value)} />
                      <Button size="xs" variant="outline" color={changePassBtn.color}
                        onClick={() => onChangePassword(newPass, newPassRe)}>
                        {changePassBtn.label}
                      </Button>
                    </Stack>
                  </Accordion.Panel>
                </Accordion.Item>
              </Accordion>
            </>
          )}
        </div>

        <Stack gap="xs">
          <Button variant="light" size="sm" onClick={onOpenHelp}>Help</Button>
          {logged && (
            <>
              <Divider />
              <Button variant="outline" color="red" onClick={onLogout}>Logout</Button>
            </>
          )}
        </Stack>
      </Stack>
    </Drawer>
  )
}