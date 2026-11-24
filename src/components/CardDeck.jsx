import { useRef, useState } from 'react';
import horses from '../data/horses';
import Card from './Card';
import LikedHorses from './LikedHorses';
import MatchOverlay from './MatchOverlay';
import ProfileModal from './ProfileModal';
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
  const [selectedHorse, setSelectedHorse] = useState(null);
  const [liked, setLiked] = useState([]);
  const [matchedHorse, setMatchedHorse] = useState(null);
  const [showLiked, setShowLiked] = useState(false);
  const [dragX, setDragX] = useState(0);
  const startX = useRef(0);
  const deltaX = useRef(0);
  const dragging = useRef(false);
  const timeoutRef = useRef(null);
  const swipeDone = useRef(true);
  const swipeDirRef = useRef(null);
  const swipeCardRef = useRef(null);
  const dragExit = useRef(false);

  const finishSwipe = () => {
    if (swipeDone.current) return;
    swipeDone.current = true;
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    if (swipeDirRef.current === 'right' && swipeCardRef.current) {
      const horse = swipeCardRef.current;
      setLiked((prev) => [...prev, horse]);
      if (Math.random() < 0.33) {
        setMatchedHorse(horse);
      }
    }
    swipeDirRef.current = null;
    swipeCardRef.current = null;
    dragExit.current = false;
    deltaX.current = 0;
    setDeck((d) => d.slice(1));
    setLeavingCard(null);
    setAnimating(null);
    setDragX(0);
  };

  const triggerSwipe = (direction) => {
    if (animating !== null) return;
    const fromDrag = Math.abs(deltaX.current) > SWIPE_THRESHOLD;
    swipeDone.current = false;
    swipeDirRef.current = direction;
    swipeCardRef.current = deck[0];
    dragExit.current = fromDrag;
    if (fromDrag) {
      // Continue the exit from the dragged position instead of letting the
      // keyframes snap the card back to centre first. The inline transform
      // transitions to the off-screen target while the keyframe animation is
      // disabled for this card.
      const distance =
        (typeof window !== 'undefined' ? window.innerWidth : 1200) * 1.2;
      setDragX(direction === 'right' ? distance : -distance);
    }
    setLeavingCard(deck[0]);
    setAnimating(direction);
    timeoutRef.current = setTimeout(finishSwipe, 300);
  };

  const handlePointerDown = (e) => {
    startX.current = e.clientX;
    deltaX.current = 0;
    dragging.current = true;
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e) => {
    if (!dragging.current) return;
    deltaX.current = e.clientX - startX.current;
    setDragX(deltaX.current);
  };

  const handlePointerUp = () => {
    dragging.current = false;
    if (Math.abs(deltaX.current) > SWIPE_THRESHOLD) {
      triggerSwipe(deltaX.current > 0 ? 'right' : 'left');
    } else {
      if (Math.abs(deltaX.current) < 10 && animating === null && deck.length > 0) {
        setSelectedHorse(deck[0]);
      }
      deltaX.current = 0;
      setDragX(0);
    }
  };

  const handleReset = () => {
    setDeck(shuffleDeck(horses));
    setLeavingCard(null);
    setAnimating(null);
    setLiked([]);
    setMatchedHorse(null);
  };

  const isEmpty = deck.length === 0 && !leavingCard && !animating;

  const dragTilt = Math.max(-12, Math.min(12, dragX * 0.06));
  const isDragExit = animating !== null && dragExit.current;
  const exitTilt = animating === 'right' ? 15 : -15;
  const stackStyles = [
    {
      zIndex: 30,
      transform: isDragExit
        ? `translateX(${dragX}px) rotate(${exitTilt}deg)`
        : `translateX(${dragX}px) rotate(${dragTilt}deg)`,
      transition: isDragExit
        ? 'transform 300ms ease-out'
        : dragging.current
          ? 'none'
          : 'transform 200ms ease-out',
      animation: isDragExit ? 'none' : undefined,
    },
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
        <>
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
          <div className="swipe-actions">
            <button
              className="swipe-btn swipe-btn-reject"
              onClick={() => triggerSwipe('left')}
              aria-label="Reject"
              type="button"
            >
              ✕
            </button>
            <button
              className="swipe-btn swipe-btn-accept"
              onClick={() => triggerSwipe('right')}
              aria-label="Like"
              type="button"
            >
              ♥
            </button>
          </div>
        </>
      )}
      <button className="liked-nav-btn" onClick={() => setShowLiked((s) => !s)}>Liked ({liked.length})</button>
      {showLiked && <LikedHorses horses={liked} />}
      <ProfileModal horse={selectedHorse} onClose={() => setSelectedHorse(null)} />
      <MatchOverlay horse={matchedHorse} onClose={() => setMatchedHorse(null)} />
    </div>
  );
}
