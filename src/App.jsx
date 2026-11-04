import { useEffect } from 'react'
import horses from './data/horses'
import './App.css'

export default function App() {
  useEffect(() => {
    console.log('horses loaded:', horses)
  }, [])

  return (
    <div className="app">
      <h1>Horse Tinder Demo</h1>
      <p>{horses.length} horses looking for love</p>
      <ul>
        {horses.map((h) => (
          <li key={h.id}>
            {h.name} — {h.breed}
          </li>
        ))}
      </ul>
    </div>
  )
}
