// Gold node-link logo mark (brand-system glyph). Shared by the navbar and the
// login gate. Color follows the Mantine gold primary.
export default function LogoMark({ size = 28 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <g stroke="var(--mantine-color-yellow-4)" strokeWidth="1.6" strokeLinecap="round" opacity="0.5">
        <line x1="10.5" y1="16" x2="24" y2="7.5" />
        <line x1="10.5" y1="16" x2="24.5" y2="24" />
        <line x1="24" y1="7.5" x2="24.5" y2="24" />
      </g>
      <circle cx="10.5" cy="16" r="5" fill="var(--mantine-color-yellow-4)" />
      <circle cx="24" cy="7.5" r="3.4" fill="var(--mantine-color-yellow-4)" />
      <circle cx="24.5" cy="24" r="2.8" fill="var(--mantine-color-yellow-4)" />
    </svg>
  )
}
