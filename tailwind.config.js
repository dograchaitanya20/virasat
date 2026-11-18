/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
    './apps/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        heritage: {
          sandstone: '#F5EFEB',
          gold: '#D4AF37',
          saffron: '#FF8F00',
          terracotta: '#C85A32',
          indigo: '#0D1322',
          peacock: '#0D5C75',
          ruby: '#9B111E',
        }
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        cinzel: ['"Cinzel"', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
        devanagari: ['"Noto Sans Devanagari"', 'sans-serif'],
      }
    }
  },
  plugins: [],
  safelist: [
    'bg-emerald-900/90', 'border-emerald-500', 'text-emerald-100',
    'bg-rose-900/90', 'border-rose-500', 'text-rose-100',
    'bg-amber-900/90', 'border-amber-500', 'text-amber-100',
    'bg-slate-900/90', 'border-amber-500/50', 'text-slate-100',
    'translate-y-4', '-translate-y-2', 'opacity-0', 'nav-scrolled'
  ]
}
