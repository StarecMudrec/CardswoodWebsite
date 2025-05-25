// src/api/index.js

// Fetch all seasons
export const fetchSeasons = async () => {
  const response = await fetch('/api/seasons')
  if (!response.ok) throw new Error('Failed to fetch seasons')
  const seasonIds = await response.json()

  const seasons = await Promise.all(
    seasonIds.map(async seasonId => {
      const seasonResponse = await fetch(`/api/season_info/${seasonId}`)
      if (!seasonResponse.ok) throw new Error('Failed to fetch season info')
      return seasonResponse.json()
    })
  )
  
  return seasons
}

// Fetch cards for a specific season
export const fetchCardsForSeason = async (seasonUuid) => {
  const response = await fetch(`/api/cards/${seasonUuid}`)
  if (!response.ok) throw new Error('Failed to fetch cards')
  const cardUuids = await response.json()
  
  const cards = await Promise.all(
    cardUuids.map(async uuid => {
      const cardResponse = await fetch(`/api/card_info/${uuid}`)
      if (!cardResponse.ok) throw new Error('Failed to fetch card info')
      return cardResponse.json()
    })
  )
  
  return cards
}

// Fetch detailed card info
export const fetchCardInfo = async (cardUuid) => {
  const response = await fetch(`/api/card_info/${cardUuid}`)
  if (!response.ok) throw new Error('Failed to fetch card info')
  return response.json()
}

// Fetch season info
export const fetchSeasonInfo = async (seasonId) => {
  const response = await fetch(`/api/season_info/${seasonId}`)
  if (!response.ok) throw new Error('Failed to fetch season info')
  return response.json()
}

// Update season info
export const updateSeason = async (seasonId, data) => {
  const response = await fetch(`/api/seasons/${seasonId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
  if (!response.ok) throw new Error('Failed to update season')
  return response.json()
}

// Fetch comments for a card
export const fetchComments = async (cardId) => {
  const response = await fetch(`/api/comments/${cardId}`)
  if (!response.ok) throw new Error('Failed to fetch comments')
  return response.json()
}

export const checkAuth = async () => {
  try {
    const response = await fetch('/api/check_auth')
    if (!response.ok) throw new Error('Auth check failed')
    return await response.json()
  } catch (error) {
    console.error('Auth check error:', error)
    return { isAuthenticated: false, userId: null }
  }
} 

// Delete a card
export const deleteCard = async (cardId) => {
  const response = await fetch(`/api/cards/${cardId}`, {
    method: 'DELETE'
  });
  if (!response.ok) throw new Error('Failed to delete card');
};

// Check user permission
export const checkUserPermission = async (username) => {
  try {
    const response = await fetch(`/api/check_permission?username=${username}`);
    if (!response.ok) throw new Error('Permission check failed');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Permission check error:', error);
    return false; // Assume not allowed on error
  }
};

// Fetch user information
export const fetchUserInfo = async () => {
  const response = await fetch('/api/user');
  if (!response.ok) throw new Error('Failed to fetch user info');
  return response.json();
};

// Create a new season
export const createSeason = async () => {
  const response = await fetch('/api/seasons', {
    method: 'POST'
  });
  if (!response.ok) throw new Error('Failed to create season');
  return response.json();
};

// Delete a season
export const deleteSeason = async (seasonUuid) => {
  const response = await fetch(`/api/seasons/${seasonUuid}`, {
    method: 'DELETE'
  });
  if (!response.ok) throw new Error('Failed to delete season');
};
