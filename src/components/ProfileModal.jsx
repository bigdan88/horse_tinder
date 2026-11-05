import './ProfileModal.css';

export default function ProfileModal({ horse, onClose }) {
  if (!horse) return null;

  return (
    <div className="profile-overlay" onClick={onClose}>
      <div className="profile-modal" onClick={(e) => e.stopPropagation()}>
        <img src={horse.imageUrl} alt={horse.name} className="profile-photo" />
        <h2>{horse.name}</h2>
        <p className="profile-breed">{horse.breed}</p>
        <p className="profile-age">{horse.age} years</p>
        <p className="profile-bio">{horse.bio}</p>
        <button className="profile-close" onClick={onClose}>
          ✕ Close
        </button>
      </div>
    </div>
  );
}
