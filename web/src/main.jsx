import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

createRoot(document.getElementById('goc')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
