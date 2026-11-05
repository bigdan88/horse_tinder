export default function Card({ horse, zIndex = 1, style = {}, className = '' }) {
  return (
    <div className={'card ' + className} style={{ zIndex, ...style }}>
      <img src={horse.imageUrl} alt={horse.name} />
      <div className="card-info">
        <h2>{horse.name}</h2>
        <p className="breed">{horse.breed}</p>
        <p className="age">{horse.age} years</p>
      </div>
    </div>
  );
}
