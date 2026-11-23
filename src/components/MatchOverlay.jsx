import './MatchOverlay.css';

export default function MatchOverlay({ horse, onClose }) {
  if (!horse) return null;

  return (
    <div className="match-overlay" onClick={onClose}>
      <div className="match-card" onClick={(e) => e.stopPropagation()}>
        <h2>It's a Match!</h2>
        <img src={horse.imageUrl} alt={horse.name} className="match-photo" />
        <p className="match-name">{horse.name}</p>
        <button className="match-close" onClick={onClose}>✕ Close</button>
      </div>
    </div>
  );
}