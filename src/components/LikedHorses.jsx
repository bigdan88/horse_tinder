import './LikedHorses.css';

export default function LikedHorses({ horses }) {
  if (!horses || horses.length === 0) {
    return <p className="liked-empty">No liked horses yet</p>;
  }
  return (
    <div className="liked-grid">
      {horses.map((horse) => (
        <div className="liked-item" key={horse.id}>
          <img src={horse.imageUrl} alt={horse.name} className="liked-thumb" />
          <p>{horse.name}</p>
        </div>
      ))}
    </div>
  );
}