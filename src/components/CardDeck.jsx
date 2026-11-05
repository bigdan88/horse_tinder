import { useRef, useState } from 'react';
import horses from '../data/horses';
import Card from './Card';
import './SwipeDeck.css';

const SWIPE_THRESHOLD = 100;

function shuffleDeck(list) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export default function CardDeck() {
  const [deck, setDeck] = useState(() => shuffleDeck(horses));
  const [animating, setAnimating] = useState(null); // null | 'left' | 'right'
  const [leavingCard, setLeavingCard] = useState(null);
  const startX = useRef(0);
  const deltaX = useRef(0);
  const timeoutRef = useRef(null);
  const swipeDone = useRef(true);

  const finishSwipe = () => {
    if (swipeDone.current) return;
    swipeDone.current = true;
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setDeck((d) => d.slice(1));
    setLeavingCard(null);
    setAnimating(null);
  };

  const triggerSwipe = (direction) => {
    if (animating !== null) return;
    swipeDone.current = false;
    setLeavingCard(deck[0]);
    setAnimating(direction);
    timeoutRef.current = setTimeout(finishSwipe, 300);
  };

  const handlePointerDown = (e) => {
    startX.current = e.clientX;
    deltaX.current = 0;
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e) => {
    deltaX.current = e.clientX - startX.current;
  };

  const handlePointerUp = () => {
    if (Math.abs(deltaX.current) > SWIPE_THRESHOLD) {
      triggerSwipe(deltaX.current > 0 ? 'right' : 'left');
    } else {
      deltaX.current = 0;
    }
  };

  const handleReset = () => {
    setDeck(shuffleDeck(horses));
    setLeavingCard(null);
    setAnimating(null);
  };

  const isEmpty = deck.length === 0 && !leavingCard && !animating;

  const stackStyles = [
    { zIndex: 30 },
    { zIndex: 20, transform: 'translateY(12px) scale(0.95) rotate(-2deg)' },
    { zIndex: 10, transform: 'translateY(24px) scale(0.9) rotate(2deg)' },
  ];

  const visible = deck.slice(0, 3);

  return (
    <div>
      <div className="counter">{deck.length} cards remaining</div>
      {isEmpty ? (
        <button className="reset-btn" onClick={handleReset}>
          Reset &amp; Shuffle
        </button>
      ) : (
        <div
          className="card-deck"
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onAnimationEnd={finishSwipe}
        >
          {visible.map((horse, i) => (
            <Card
              key={horse.id}
              horse={horse}
              zIndex={stackStyles[i].zIndex}
              style={stackStyles[i]}
              className={i === 0 && animating ? (animating === 'right' ? 'swipe-right' : 'swipe-left') : ''}
            />
          ))}
        </div>
      )}
    </div>
  );
}
