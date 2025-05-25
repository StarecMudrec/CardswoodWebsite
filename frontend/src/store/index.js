import { createStore } from 'vuex'
import { fetchSeasons, checkAuth, updateSeason } from '@/api'

export default createStore({
  state: {
    isAuthenticated: false,
    userId: null,
    seasons: [],
    loading: false,
    error: null,
    selectedCards: []
  },
  mutations: {
    SET_AUTH(state, { isAuthenticated, userId }) {
      state.isAuthenticated = isAuthenticated
      state.userId = userId
    },
    SET_SEASONS(state, seasons) {
      state.seasons = seasons
    },
    UPDATE_SEASON(state, updatedSeason) {
      const index = state.seasons.findIndex(s => s.uuid === updatedSeason.uuid);
      if (index !== -1) {
        state.seasons.splice(index, 1, updatedSeason);
      }
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_SELECTED_CARDS(state, cards) {
      state.selectedCards = cards
    },
    ADD_SELECTED_CARD(state, cardId) {
      if (!state.selectedCards.includes(cardId)) {
        state.selectedCards.push(cardId)
      }
    },
    REMOVE_SELECTED_CARD(state, cardId) {
      state.selectedCards = state.selectedCards.filter(id => id !== cardId)
    },
    CLEAR_SELECTED_CARDS(state) {
      state.selectedCards = []
    }
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        const { isAuthenticated, userId } = await checkAuth()
        commit('SET_AUTH', { isAuthenticated, userId })
        return { isAuthenticated, userId }
      } catch (error) {
        console.error('Auth check failed:', error)
        throw error
      }
    },

    async logout({ commit }) {
      try {
        await fetch('/auth/logout', { 
          method: 'POST',
          credentials: 'include'
        })
        commit('SET_AUTH', { isAuthenticated: false, userId: null })
        commit('CLEAR_SELECTED_CARDS')
      } catch (error) {
        console.error('Logout failed:', error)
        throw error
      }
    },

    async fetchSeasons({ commit }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      try {
        const response = await fetch('/api/seasons')
        if (!response.ok) throw new Error('Failed to fetch season IDs')
        
        const seasonIds = await response.json()
        const seasonPromises = seasonIds.map(id => 
          fetch(`/api/season_info/${id}`)
            .then(res => {
              if (!res.ok) throw new Error(`Failed to fetch season ${id}`)
              return res.json()
            })
        )
        
        const seasons = await Promise.all(seasonPromises)
        commit('SET_SEASONS', seasons)
        return seasons
      } catch (error) {
        commit('SET_ERROR', error)
        console.error('Error fetching seasons:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async updateSeason({ commit }, seasonData) {
      try {
        const updatedSeason = await updateSeason(seasonData.uuid, { name: seasonData.name });
        commit('UPDATE_SEASON', updatedSeason);
        return updatedSeason;
      } catch (error) {
        console.error('Error updating season:', error);
        throw error;
      }
    },

    async deleteSelectedCards({ state, commit, dispatch }) {
      try {
        commit('SET_LOADING', true)
        await Promise.all(
          state.selectedCards.map(cardId => 
            fetch(`/api/cards/${cardId}`, { method: 'DELETE' })
          )
        )
        commit('CLEAR_SELECTED_CARDS')
        await dispatch('fetchSeasons') // Refresh data
      } catch (error) {
        commit('SET_ERROR', error)
        console.error('Error deleting cards:', error)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    toggleCardSelection({ commit, state }, cardId) {
      if (state.selectedCards.includes(cardId)) {
        commit('REMOVE_SELECTED_CARD', cardId)
      } else {
        commit('ADD_SELECTED_CARD', cardId)
      }
    }
  },
  getters: {
    isUserAllowed: state => state.isAuthenticated,
    getSeasonById: state => id => state.seasons.find(season => season.uuid === id),
    selectedCardsCount: state => state.selectedCards.length
  }
})