/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
  ],
  darkMode: 'class',
  safelist: [
  'w-full','border','rounded','px-3','py-2','text-sm','bg-white','shadow',
  'text-red-500','text-gray-600','bg-brand-primary','hover:bg-brand-secondary',
  'font-medium','max-w-sm','mx-auto','mt-10','p-6',
  // Nuevos estilos para inputs y estados de focus del login/signup (se definen en Python, no escaneados por Tailwind)
  'focus:outline-none','focus:ring-2','focus:ring-brand-primary','focus:border-brand-primary',
  'border-brand-primary','bg-brand-light','text-brand-secondary','text-brand-dark','transition',
  // Sidebar dynamic classes (agregadas via JS)
  'active-link','bg-brand-primary/15','dark:bg-gray-800','dark:text-brand-primary','border-l-2'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#E8B923',
          secondary: '#DD3F2E',
          dark: '#161616',
          light: '#F2F2F2'
        }
      }
    },
  },
  plugins: [],
};