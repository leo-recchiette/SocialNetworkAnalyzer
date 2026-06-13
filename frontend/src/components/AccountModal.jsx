import { useState } from 'react'
import { Button, Divider, Modal, PasswordInput, Stack, Text, TextInput } from '@mantine/core'

// Account settings modal, opened from the navbar account menu.
// Holds the change-password (and retained change-email) forms; feedback flips
// the action buttons via changePassBtn / changeMailBtn, same as before.
export default function AccountModal({
  opened, onClose, usr,
  onChangeMail, onChangePassword, changeMailBtn, changePassBtn,
}) {
  const [newMail, setNewMail] = useState('')
  const [newMailRe, setNewMailRe] = useState('')
  const [newPass, setNewPass] = useState('')
  const [newPassRe, setNewPassRe] = useState('')

  return (
    <Modal opened={opened} onClose={onClose} title={<b>Account</b>} centered size="md">
      <Stack gap="lg">
        <Text size="sm" c="dimmed">Signed in as <b>{usr}</b></Text>

        <div>
          <Text fw={700} size="sm" mb="xs">Change your password</Text>
          <Stack gap="xs">
            <PasswordInput
              placeholder="Insert new password"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>vpn_key</i>}
              value={newPass}
              onChange={(e) => setNewPass(e.currentTarget.value)}
            />
            <PasswordInput
              placeholder="Retype new password"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>vpn_key</i>}
              value={newPassRe}
              onChange={(e) => setNewPassRe(e.currentTarget.value)}
            />
            <Button variant="outline" color={changePassBtn.color}
              onClick={() => onChangePassword(newPass, newPassRe)}>
              {changePassBtn.label}
            </Button>
          </Stack>
        </div>

        <Divider />

        <div>
          <Text fw={700} size="sm" mb="xs">Change your email</Text>
          <Stack gap="xs">
            <TextInput
              placeholder="Insert new email"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>mail</i>}
              value={newMail}
              onChange={(e) => setNewMail(e.currentTarget.value)}
            />
            <TextInput
              placeholder="Retype new email"
              leftSection={<i className="material-icons" style={{ fontSize: 16 }}>mail</i>}
              value={newMailRe}
              onChange={(e) => setNewMailRe(e.currentTarget.value)}
            />
            <Button variant="outline" color={changeMailBtn.color}
              onClick={() => onChangeMail(newMail, newMailRe)}>
              {changeMailBtn.label}
            </Button>
          </Stack>
        </div>
      </Stack>
    </Modal>
  )
}
