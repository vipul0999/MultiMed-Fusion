// src/utils/utils.js

/**
 * Format a date into a readable string
 * @param {string | Date} date
 * @returns {string}
 */
export function formatDate(date) {
  const d = new Date(date);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Capitalize the first letter of a string
 * @param {string} str
 * @returns {string}
 */
export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Generate a random ID (useful for keys or temporary identifiers)
 * @param {number} length
 * @returns {string}
 */
export function generateId(length = 8) {
  return Math.random().toString(36).substring(2, 2 + length);
}

/**
 * Debounce a function — ensures it's only called after a delay
 * @param {Function} func
 * @param {number} delay
 * @returns {Function}
 */
export function debounce(func, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => func(...args), delay);
  };
}
