export interface Horse {
  id: number;
  name: string;
  breed: string;
  age: number;
  bio: string;
  imageUrl: string;
}

export const horses: Horse[] = [
  {
    id: 1,
    name: 'Sir Gallops-a-Lot',
    breed: 'Thoroughbred',
    age: 7,
    bio: 'Retired racehorse convinced every hallway is a track. Holds the barn record for most dramatic slow-motion trot.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23e74c3c'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Sir Gallops-a-Lot</text></svg>",
  },
  {
    id: 2,
    name: 'Buttercup Bramblewood',
    breed: 'Haflinger',
    age: 12,
    bio: 'Golden-maned and gloriously round. Will trade affection for apples at a rate of one apple per nuzzle.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23f39c12'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Buttercup Bramblewood</text></svg>",
  },
  {
    id: 3,
    name: 'Duchess of Neigh',
    breed: 'Friesian',
    age: 10,
    bio: 'Flowing black mane, aristocratic snort. Refuses to step in puddles because mud is for commoners.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%238e44ad'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Duchess of Neigh</text></svg>",
  },
  {
    id: 4,
    name: 'Taco',
    breed: 'Appaloosa',
    age: 5,
    bio: 'Spotted like a sprinkle donut and twice as sweet. Believes every fence is a personal suggestion.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%2316a085'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Taco</text></svg>",
  },
  {
    id: 5,
    name: 'Baron Von Whinny',
    breed: 'Clydesdale',
    age: 14,
    bio: 'Feathered feet the size of dinner plates. Gentle giant who is scared of one (1) specific chicken.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%232980b9'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Baron Von Whinny</text></svg>",
  },
  {
    id: 6,
    name: 'Peanut Buttercup',
    breed: 'Shetland Pony',
    age: 9,
    bio: 'Small, sticky, and unstoppable. Has never once respected a personal boundary or an electric fence.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23d35400'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Peanut Buttercup</text></svg>",
  },
  {
    id: 7,
    name: 'Moonshadow Dancer',
    breed: 'Arabian',
    age: 6,
    bio: 'Tail carried like a flag at a parade. Prances even when standing still, which is technically levitation.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23343a40'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Moonshadow Dancer</text></svg>",
  },
  {
    id: 8,
    name: 'Chesterfield',
    breed: 'Percheron',
    age: 16,
    bio: 'Distinguished grey gentleman who has seen things. Mostly carrots, but also some things.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%2395a5a6'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Chesterfield</text></svg>",
  },
  {
    id: 9,
    name: 'Waffles',
    breed: 'Paint Horse',
    age: 4,
    bio: 'Young, chaotic, syrup-colored. Her bucket list is just the word "run" written eleven times.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23f1c40f'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Waffles</text></svg>",
  },
  {
    id: 10,
    name: 'Lady Cinnamon Swirl',
    breed: 'Rocky Mountain Horse',
    age: 11,
    bio: 'Chocolate coat, caramel attitude. Judges your posture from across the paddock.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%237f5539'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Lady Cinnamon Swirl</text></svg>",
  },
  {
    id: 11,
    name: 'Ziggy Stardust',
    breed: 'Gypsy Vanner',
    age: 8,
    bio: 'Piebald, flamboyant, here for a good time. His mane has its own gravitational field.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23c0392b'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Ziggy Stardust</text></svg>",
  },
  {
    id: 12,
    name: 'Old Man Jenkins',
    breed: 'Quarter Horse',
    age: 24,
    bio: 'Seen it all, done most of it, napped through the rest. Moves at exactly one speed: eventually.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23bdc3c7'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Old Man Jenkins</text></svg>",
  },
  {
    id: 13,
    name: 'Biscuit',
    breed: 'Icelandic Horse',
    age: 3,
    bio: 'Tiny, fluffy, absolutely certain she is a wolf. Tölts faster than your WiFi.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%23e67e22'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Biscuit</text></svg>",
  },
  {
    id: 14,
    name: 'Comet Thunderhoof',
    breed: 'Mustang',
    age: 13,
    bio: 'Born wild, stays wild, occasionally visits civilization for snacks and gossip.',
    imageUrl:
      "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400'><rect width='100%25' height='100%25' fill='%232c3e50'/><text x='50%25' y='50%25' text-anchor='middle' font-size='40'>🐴</text><text x='50%25' y='70%25' text-anchor='middle' font-size='16'>Comet Thunderhoof</text></svg>",
  },
];

export default horses;
