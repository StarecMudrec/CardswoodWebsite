// src/api/index.js
import axios from 'axios'

// Fetch all seasons
export const fetchSeasons = async () => {
  const response = await fetch('/api/seasons')
  if (!response.ok) throw new Error('Не удалось получить список сезонов')
  const seasonIds = await response.json()

  const seasons = await Promise.all(
    seasonIds.map(async seasonId => {
      const seasonResponse = await fetch(`/api/season_info/${seasonId}`)
      if (!seasonResponse.ok) throw new Error('Не удалось получить информацию о сезоне')
      return seasonResponse.json()
    })
  )
  
  return seasons
}

// Create a donation and receive PayAnyWay payment URL
export const createDonation = async (amount, description = 'Donation') => {
  const response = await fetch('/api/donations/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ amount, description })
  })

  if (!response.ok) {
    let message = 'Не удалось создать платёж'
    try {
      const errorBody = await response.json()
      if (errorBody && errorBody.error) {
        message = errorBody.error
      }
    } catch (e) {
      // ignore JSON parsing errors
    }
    throw new Error(message)
  }

  return response.json()
}

// Fetch cards for a specific season
export async function fetchCardsForSeason(seasonId, sortField = 'id', sortDirection = 'asc') {
  try {
    const response = await axios.get(`/api/cards/${seasonId}`, {
      params: {
        sort: sortField,
        direction: sortDirection
      }
    });
    
    // Transform the data to match what your Card component expects
    return response.data.map(card => ({
      id: card.id,
      uuid: card.uuid || card.id.toString(), // Fallback to id if uuid doesn't exist
      img: card.photo || card.img,           // Handle different field names
      name: card.name,
      rarity: card.rarity,
      points: card.points,
      category: card.rarity,                 // Map rarity to category if needed
      // Include any other required fields
    }));
    
  } catch (error) {
    console.error('Ошибка получения карточек:', error);
    throw error;
  }
}

// Fetch detailed card info
export const fetchCardInfo = async (cardId) => {
  const response = await fetch(`/api/card_info/${cardId}`)
  if (!response.ok) throw new Error('Не удалось получить информацию о карточке')
  return response.json()
}

// Fetch season info
export const fetchSeasonInfo = async (seasonId) => {
  const response = await fetch(`/api/season_info/${seasonId}`)
  if (!response.ok) throw new Error('Не удалось получить информацию о сезоне')
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
  if (!response.ok) throw new Error('Не удалось обновить сезон')
  return response.json()
}

// Fetch comments for a card
export const fetchComments = async (cardId) => {
  const response = await fetch(`/api/comments/${cardId}`)
  if (!response.ok) throw new Error('Не удалось получить комментарии')
  return response.json()
}

export const checkAuth = async () => {
  try {
    const response = await fetch('/api/check_auth')
    if (!response.ok) throw new Error('Не удалось проверить авторизацию')
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
  if (!response.ok) throw new Error('Не удалось удалить карточку');
};

// Check user permission
export const checkUserPermission = async (username) => {
  try {
    const response = await fetch(`/api/check_permission?username=${username}`);
    if (!response.ok) throw new Error('Не удалось проверить права доступа');
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
  if (!response.ok) throw new Error('Не удалось получить данные пользователя');
  return response.json();
};

// Create a new season
export const createSeason = async () => {
  const response = await fetch('/api/seasons', {
    method: 'POST'
  });
  if (!response.ok) throw new Error('Не удалось создать сезон');
  return response.json();
};

// Delete a season
export const deleteSeason = async (seasonUuid) => {
  const response = await fetch(`/api/seasons/${seasonUuid}`, {
    method: 'DELETE'
  });
  if (!response.ok) throw new Error('Не удалось удалить сезон');
};
