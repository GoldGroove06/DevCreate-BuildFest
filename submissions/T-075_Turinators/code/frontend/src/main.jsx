import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Navbar from './components/Navbar.jsx'
import Sidebar from './components/Sidebar.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar/>
    <div className='flex flex-row  w-full'>
      <div className='w-full'>
<App />
      </div>
   
    </div>
         
  </StrictMode>,
)
