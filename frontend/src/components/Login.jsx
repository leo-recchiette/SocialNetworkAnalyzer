import { useState } from 'react'
import {
  Anchor, Box, Button, Divider, Group, PasswordInput, SegmentedControl,
  Stack, Text, TextInput, Title,
} from '@mantine/core'

import LogoMark from './LogoMark.jsx'

// Decorative faint node-link constellation behind the brand panel (styles in styles.css).
function Constellation() {
  const nodes = [
    [60, 90], [180, 60], [120, 200], [260, 170], [330, 90], [300, 280], [160, 330],
    [410, 200], [70, 300], [230, 420], [380, 360], [120, 440], [300, 440], [440, 310],
  ]
  const links = [
    [0, 1], [0, 2], [1, 3], [1, 4], [2, 3], [2, 8], [3, 7], [4, 7], [5, 3],
    [5, 10], [6, 2], [6, 9], [7, 13], [9, 11], [10, 13], [5, 12], [9, 6], [11, 12],
  ]
  return (
    <svg className="sna-constellation" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid slice"
      aria-hidden="true" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
      {links.map(([a, b], i) => (
        <line key={'l' + i} x1={nodes[a][0]} y1={nodes[a][1]} x2={nodes[b][0]} y2={nodes[b][1]} />
      ))}
      {nodes.map(([x, y], i) => (
        <circle key={'n' + i} className="n" cx={x} cy={y} r={2.5 + (i % 3) * 1.6} />
      ))}
    </svg>
  )
}

const icon = (n) => <i className="material-icons" style={{ fontSize: 16 }}>{n}</i>

// Full-screen authentication gate shown while logged out (usr === '').
// Reuses App's auth handlers and feedback channels verbatim:
//  - login errors surface inline via loginFeedback ({ field: 'mail'|'password', msg })
//  - register feedback flips the submit button via registerBtn ({ color, label })
export default function Login({ onLogin, onRegister, loginFeedback, registerBtn }) {
  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [mail, setMail] = useState('')
  const [password, setPassword] = useState('')

  const isRegister = mode === 'register'

  function submit() {
    if (isRegister) onRegister(mail, password)
    else onLogin(mail, password)
  }
  const onKeyDown = (e) => { if (e.key === 'Enter') submit() }

  return (
    <Box style={{ minHeight: '100vh', display: 'grid', gridTemplateColumns: '1.1fr 1fr' }}>
      {/* Brand panel */}
      <Box visibleFrom="sm" style={{
        position: 'relative', overflow: 'hidden',
        background: 'var(--mantine-color-dark-8)',
        borderRight: '1px solid var(--mantine-color-dark-4)',
        padding: 48, display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
      }}>
        <Constellation />
        <Group gap="xs" style={{ position: 'relative' }}>
          <LogoMark />
          <Text fw={700} fz={20} c="white">SNA Analyzer</Text>
        </Group>
        <Box style={{ position: 'relative' }}>
          <Title order={1} c="white" style={{ lineHeight: 1.1 }}>
            Map the network<br />behind the data.
          </Title>
          <Text c="dark.2" mt="md" maw={440}>
            Forensic analysis of Facebook, Twitter and mailbox dumps — relationships,
            message traffic, geography and language.
          </Text>
          <Group gap={6} mt="xl">
            {['relationships', 'traffic', 'geo', 'word frequency'].map((t) => (
              <Text key={t} span ff="monospace" fz={11} px={8} py={3}
                style={{ border: '1px solid var(--mantine-color-dark-4)', color: 'var(--mantine-color-dark-1)' }}>
                {t}
              </Text>
            ))}
          </Group>
        </Box>
      </Box>

      {/* Form panel */}
      <Box style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: 32, background: 'var(--mantine-color-dark-7)',
      }}>
        <Stack w="100%" maw={360} gap="md">
          <Stack gap={4}>
            <Title order={3} c="white">{isRegister ? 'Create account' : 'Sign in'}</Title>
            <Text fz="sm" c="dark.2">
              {isRegister
                ? 'Register to upload and analyse your dumps.'
                : 'Access your network analysis workspace.'}
            </Text>
          </Stack>

          <SegmentedControl
            fullWidth
            value={mode}
            onChange={setMode}
            data={[{ label: 'Sign in', value: 'login' }, { label: 'Register', value: 'register' }]}
          />

          <TextInput
            label="Email"
            placeholder="Insert email"
            leftSection={icon('mail')}
            value={mail}
            onChange={(e) => setMail(e.currentTarget.value)}
            onKeyDown={onKeyDown}
            error={!isRegister && loginFeedback.field === 'mail' ? loginFeedback.msg : null}
          />
          <PasswordInput
            label="Password"
            placeholder="Insert password"
            autoComplete={isRegister ? 'new-password' : 'current-password'}
            leftSection={icon('vpn_key')}
            value={password}
            onChange={(e) => setPassword(e.currentTarget.value)}
            onKeyDown={onKeyDown}
            error={!isRegister && loginFeedback.field === 'password' ? loginFeedback.msg : null}
          />

          {isRegister ? (
            <Button fullWidth color={registerBtn.color} onClick={submit}>
              {registerBtn.label}
            </Button>
          ) : (
            <Button fullWidth leftSection={icon('login')} onClick={submit}>
              Login
            </Button>
          )}

          <Divider label={isRegister ? 'already registered?' : 'no account yet?'} labelPosition="center" />
          <Anchor ta="center" fz="sm" onClick={() => setMode(isRegister ? 'login' : 'register')}>
            {isRegister ? 'Back to sign in' : 'Create an account'}
          </Anchor>
        </Stack>
      </Box>
    </Box>
  )
}
