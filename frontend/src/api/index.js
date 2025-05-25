// src/api/index.js

// Base API URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

/**
 * Helper function for API requests
 */
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    credentials: 'include'
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `API request failed: ${response.statusText}`);
  }

  return response.json();
};

// Fetch all seasons
export const fetchSeasons = async () => {
  const seasonIds = await apiRequest('/seasons');
  const seasons = await Promise.all(
    seasonIds.map(seasonId => apiRequest(`/season_info/${seasonId}`))
  );
  return seasons;
};

// Fetch cards for a specific season
export const fetchCardsForSeason = async (seasonUuid) => {
  const cardUuids = await apiRequest(`/cards/${seasonUuid}`);
  const cards = await Promise.all(
    cardUuids.map(uuid => apiRequest(`/card_info/${uuid}`))
  );
  return cards;
};

// Fetch detailed card info
export const fetchCardInfo = async (cardUuid) => {
  return apiRequest(`/card_info/${cardUuid}`);
};

// Fetch season info
export const fetchSeasonInfo = async (seasonId) => {
  return apiRequest(`/season_info/${seasonId}`);
};

// Update season info
export const updateSeason = async (seasonUuid, updateData) => {
  return apiRequest(`/seasons/${seasonUuid}`, {
    method: 'PUT',
    body: JSON.stringify(updateData)
  });
};

// Fetch comments for a card
export const fetchComments = async (cardId) => {
  return apiRequest(`/comments/${cardId}`);
};

// Authentication check
export const checkAuth = async () => {
  try {
    return await apiRequest('/check_auth');
  } catch (error) {
    console.error('Auth check error:', error);
    return { isAuthenticated: false, userId: null };
  }
};

// User logout
export const logout = async () => {
  return apiRequest('/auth/logout', {
    method: 'POST'
  });
};

// Delete a card
export const deleteCard = async (cardId) => {
  return apiRequest(`/cards/${cardId}`, {
    method: 'DELETE'
  });
};

// Delete multiple cards
export const deleteCards = async (cardIds) => {
  return apiRequest('/cards/batch_delete', {
    method: 'POST',
    body: JSON.stringify({ cardIds })
  });
};

// Check user permission
export const checkUserPermission = async (username) => {
  try {
    return await apiRequest(`/check_permission?username=${username}`);
  } catch (error) {
    console.error('Permission check error:', error);
    return false;
  }
};

// Fetch user information
export const fetchUserInfo = async () => {
  return apiRequest('/user');
};

// Create a new season
export const createSeason = async () => {
  return apiRequest('/seasons', {
    method: 'POST'
  });
};

// Create a new card
export const createCard = async (cardData) => {
  return apiRequest('/cards', {
    method: 'POST',
    body: JSON.stringify(cardData)
  });
};

// Update card info
export const updateCard = async (cardUuid, updateData) => {
  return apiRequest(`/cards/${cardUuid}`, {
    method: 'PUT',
    body: JSON.stringify(updateData)
  });
};

// Upload card image
export const uploadCardImage = async (cardUuid, imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  return apiRequest(`/cards/${cardUuid}/image`, {
    method: 'POST',
    body: formData,
    headers: {} // Let browser set Content-Type with boundary
  });
};