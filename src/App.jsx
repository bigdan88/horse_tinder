import horses from './data/horses'
import CardDeck from './components/CardDeck'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <h1>Horse Tinder Demo</h1>
      <p className="tagline">{horses.length} horses looking for love</p>
      <CardDeck />
    </div>
  )
}
