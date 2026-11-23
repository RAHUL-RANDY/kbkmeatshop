export const CATEGORIES = [
  {
    id: 'chicken',
    title: 'Fresh Chicken',
    subtitle: 'Hygienic & Farm Fresh',
    image: '/images/cat-chicken.jpg',
    itemCount: '18 Items',
    badge: 'Farm Raised',
    tag: '100% Natural'
  },
  {
    id: 'mutton',
    title: 'Fresh Mutton',
    subtitle: 'Tender & High Quality',
    image: '/images/cat-mutton.jpg',
    itemCount: '12 Items',
    badge: 'Premium Cut',
    tag: 'Grass Fed'
  },
  {
    id: 'fish',
    title: 'Fresh Fish',
    subtitle: 'Daily Catch & Cleaned',
    image: '/images/cat-fish.jpg',
    itemCount: '15 Items',
    badge: 'Daily Catch',
    tag: 'Chemical Free'
  },
  {
    id: 'eggs',
    title: 'Farm Fresh Eggs',
    subtitle: 'Nutritious & Chemical Free',
    image: '/images/cat-eggs.jpg',
    itemCount: '8 Packs',
    badge: 'Free Range',
    tag: 'Organic'
  }
];

export const PRODUCTS = [
  {
    id: 'country-chicken',
    name: 'Country Chicken',
    category: 'chicken',
    price: 320,
    originalPrice: 380,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg', '2 kg'],
    defaultWeight: '1 kg',
    isBestseller: true,
    rating: 4.9,
    reviews: 428,
    image: '/images/prod-country-chicken.jpg',
    description: 'Rich, natural free-roaming country chicken with tender fibrous texture and authentic rustic flavor. No antibiotics or hormones.',
    inStock: true,
    pieces: '12-16 Pieces',
    serves: '3-4 Persons'
  },
  {
    id: 'broiler-chicken',
    name: 'Broiler Chicken',
    category: 'chicken',
    price: 220,
    originalPrice: 260,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg', '2 kg'],
    defaultWeight: '1 kg',
    isBestseller: false,
    rating: 4.8,
    reviews: 310,
    image: '/images/prod-broiler-chicken.jpg',
    description: 'Juicy and succulent chicken drumsticks and curry cuts, chilled at optimum 0-4°C to retain natural juices and tenderness.',
    inStock: true,
    pieces: '8-10 Pieces',
    serves: '2-3 Persons'
  },
  {
    id: 'chicken-breast',
    name: 'Chicken Breast',
    category: 'chicken',
    price: 380,
    originalPrice: 420,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg', '1.5 kg'],
    defaultWeight: '1 kg',
    isBestseller: false,
    rating: 4.9,
    reviews: 580,
    image: '/images/prod-chicken-breast.jpg',
    description: 'Skinless, boneless lean fillets packed with high protein. Ideal for grilling, keto diets, gym meal preps, and stir-fry recipes.',
    inStock: true,
    pieces: '4-6 Fillets',
    serves: '4 Persons'
  },
  {
    id: 'mutton-curry-cut',
    name: 'Mutton Curry Cut',
    category: 'mutton',
    price: 780,
    originalPrice: 850,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg', '2 kg'],
    defaultWeight: '1 kg',
    isBestseller: true,
    rating: 5.0,
    reviews: 692,
    image: '/images/prod-mutton-curry.jpg',
    description: 'A balance of bone-in and boneless lamb and goat cuts selected from ribs, shoulder, and leg for decadent slow-cooked curries.',
    inStock: true,
    pieces: '16-20 Pieces',
    serves: '4-5 Persons'
  },
  {
    id: 'mutton-boneless',
    name: 'Mutton Boneless',
    category: 'mutton',
    price: 980,
    originalPrice: 1080,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg', '1.5 kg'],
    defaultWeight: '1 kg',
    isBestseller: true,
    rating: 4.9,
    reviews: 385,
    image: '/images/prod-mutton-boneless.jpg',
    description: 'Uniformly diced prime chunks of pure boneless goat meat. Perfect for pan roasts, mutton biryani, kebabs, and gourmet gravies.',
    inStock: true,
    pieces: 'Bite Size Cubes',
    serves: '4 Persons'
  },
  {
    id: 'farm-fresh-eggs',
    name: 'Farm Fresh Eggs',
    category: 'eggs',
    price: 160,
    originalPrice: 190,
    unit: '30 Eggs',
    weightOptions: ['6 Eggs', '12 Eggs', '1 Pack (30 Eggs)'],
    defaultWeight: '1 Pack (30 Eggs)',
    isBestseller: true,
    rating: 4.9,
    reviews: 840,
    image: '/images/prod-farm-eggs.jpg',
    description: 'Farm-laid antibiotic-free table eggs with rich golden yolks and thick shells. Washed, graded, and quality inspected daily.',
    inStock: true,
    pieces: '30 Fresh Eggs',
    serves: 'Whole Family'
  },
  {
    id: 'salmon-steak',
    name: 'Atlantic Salmon Steak',
    category: 'fish',
    price: 650,
    originalPrice: 750,
    unit: '500 g',
    weightOptions: ['250 g', '500 g', '1 kg'],
    defaultWeight: '500 g',
    isBestseller: false,
    rating: 4.9,
    reviews: 210,
    image: '/images/prod-salmon-steak.jpg',
    description: 'Fresh Norwegian Atlantic salmon cut into uniform steaks, rich in Omega-3 fatty acids, vibrant natural color, and tender flaky texture.',
    inStock: true,
    pieces: '2-3 Thick Steaks',
    serves: '2 Persons'
  },
  {
    id: 'fresh-mackerel',
    name: 'Fresh Mackerel & Seabass',
    category: 'fish',
    price: 360,
    originalPrice: 420,
    unit: 'kg',
    weightOptions: ['500 g', '1 kg'],
    defaultWeight: '1 kg',
    isBestseller: false,
    rating: 4.7,
    reviews: 145,
    image: '/images/cat-fish.jpg',
    description: 'Daily ocean catch, whole cleaned and gutted. Ready for spicy coastal tawa fry or aromatic coconut fish curry.',
    inStock: true,
    pieces: '3-4 Whole Fish',
    serves: '3 Persons'
  }
];

export const TESTIMONIALS = [
  {
    id: 1,
    name: 'Chef Marcus Vance',
    role: 'Executive Chef, Le Bistro',
    avatar: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=150&auto=format&fit=crop&q=80',
    rating: 5,
    comment: 'The marbling on their mutton and the freshness of the country chicken is unmatched. The cold-chain delivery ensures the meat arrives at peak cellar temperature.',
    date: 'Yesterday'
  },
  {
    id: 2,
    name: 'Priya Sharma',
    role: 'Food Blogger & Home Chef',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    rating: 5,
    comment: 'I will never buy meat from ordinary butcher shops again. The glassmorphism app is gorgeous, ordering is effortless, and the packaging is 100% clean and odor-free!',
    date: '3 days ago'
  },
  {
    id: 3,
    name: 'David Reynolds',
    role: 'Fitness Coach & Athlete',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    rating: 5,
    comment: 'The boneless chicken breasts are tender, juicy, and never dry out during meal prep. 100% natural without antibiotic residues—essential for my diet.',
    date: '1 week ago'
  }
];

export const TRUST_FEATURES = [
  {
    id: 'cold-chain',
    title: '0°C to 4°C Cold Chain',
    desc: 'Constant temperature monitoring from farm to your kitchen',
    icon: 'ThermometerSnowflake'
  },
  {
    id: 'hygiene',
    title: 'Certified Farm Sourced',
    desc: '100% antibiotic & chemical residue free livestock',
    icon: 'ShieldCheck'
  },
  {
    id: 'weekend-delivery',
    title: 'Weekend Farm-Fresh Delivery',
    desc: 'Pre-book all week — farm slaughtered & delivered fresh every Saturday & Sunday morning',
    icon: 'CalendarCheck'
  },
  {
    id: 'halal',
    title: '100% Halal & Clean Cut',
    desc: 'Artisanal butchery following strict sanitary guidelines',
    icon: 'CheckCircle2'
  }
];
