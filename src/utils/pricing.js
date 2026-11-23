/**
 * Dynamic pricing calculation based on selected weight/pack size.
 * Handles:
 * - Meat per-kg scaling: 250g (0.25x), 500g (0.5x), 1kg (1.0x), 1.5kg (1.5x), 2kg (2.0x)
 * - Eggs pack scaling: 6 eggs, 12 eggs, 30 eggs
 * - Seafood 500g base scaling: 250g (0.5x), 500g (1.0x), 1kg (2.0x)
 */
export function calculatePriceForWeight(product, weightStr) {
  if (!product) return 0;
  const base = Number(product.price || 0);
  if (!weightStr || !base) return base;

  const w = weightStr.trim().toLowerCase();
  const unit = (product.unit || '').trim().toLowerCase();
  const defaultW = (product.defaultWeight || product.default_weight || '').trim().toLowerCase();

  // If base unit is 500 g (e.g. Salmon Steak @ ₹650 for 500 g)
  if (unit.includes('500') || defaultW.includes('500 g')) {
    if (w.includes('250') && w.includes('g')) return Math.round(base * 0.5);
    if (w.includes('500') && w.includes('g')) return base;
    if (w.includes('1') && w.includes('kg')) return Math.round(base * 2.0);
    if (w.includes('2') && w.includes('kg')) return Math.round(base * 4.0);
  }

  // Eggs (e.g. Farm Fresh Eggs @ ₹160 for 30 eggs)
  if (w.includes('egg') || product.category === 'eggs') {
    if (w.includes('6')) return Math.round(base * (6 / 30));
    if (w.includes('12')) return Math.round(base * (12 / 30));
    if (w.includes('30') || w.includes('1 pack')) return base;
  }

  // Standard per-kg meat items (Chicken, Mutton, Fish, etc.)
  if (w.includes('250') && w.includes('g')) {
    return Math.round(base * 0.25);
  }
  if (w.includes('500') && w.includes('g')) {
    return Math.round(base * 0.5);
  }
  if (w.includes('1.5') && w.includes('kg')) {
    return Math.round(base * 1.5);
  }
  if (w.includes('2') && w.includes('kg')) {
    return Math.round(base * 2.0);
  }
  if (w.includes('1') && w.includes('kg')) {
    return base;
  }

  return base;
}
