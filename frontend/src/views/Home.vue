<template>
  <div>
    <div class="background-container"></div>
    <img src="/logo_noph.png" alt="Logo" class="background-logo">
    <hr class="separator-line">
    <div id="seasons-container">
      <div v-if="loading" class="loading">Loading cards...</div>
      <div v-else-if="error" class="error-message">Error loading data: {{ error.message || error }}. Please try again later.</div>
      <div v-else-if="seasons.length === 0" class="loading">No seasons found</div>
      <div v-for="season in seasons" :key="season.uuid" class="season-wrapper">
        <div class="season-header">
          <h2 class="season-title">
            <span v-if="!editingSeason[season.uuid]">{{ season.name }}</span>
            <input
              v-else
              v-model="editableSeasonName"
              @blur="saveSeasonName(season)"
              @keyup.enter="saveSeasonName(season)"
              @keyup.esc="cancelEditSeason(season)"
              ref="seasonNameInput"
              class="edit-input"
            >
            <span 
              v-if="isUserAllowed" 
              class="edit-icon" 
              @click="startEditSeason(season)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </span>
          </h2>
          <button v-if="selectedCards.length > 0" @click="deleteSelectedCards" class="delete-selected-button">
            <i class="bi bi-trash"></i> ({{ selectedCards.length }})
          </button>
          <button @click="$router.push('/add-card')" class="add-card-button desktop-only">
            + Add New Card
          </button>
        </div>
        <Season 
          :season="season" 
          @card-clicked="navigateToCard"
          @add-card="navigateToAddCard"
          @emitUserAllowedStatus="updateUserAllowedStatus"
        />
      </div>
    </div>
    <div v-if="isUserAllowed" class="add-season-footer">
      <div class="add-new-season-btn" @click="navigateToAddSeason">
        + Add New Season
      </div>
    </div>
  </div>
</template>

<script>
import Season from '@/components/Season.vue'
import { mapActions, mapState } from 'vuex'

export default {
  components: {
    Season
  },
  data() {
    return {
      isUserAllowed: false,
      selectedCards: [],
      editingSeason: {},
      editableSeasonName: '',
      currentEditingSeason: null
    };
  },
  computed: {
    ...mapState(['seasons', 'loading', 'error'])
  },
  methods: {
    ...mapActions(['fetchSeasons', 'updateSeason']),
    
    startEditSeason(season) {
      this.editingSeason = { [season.uuid]: true };
      this.editableSeasonName = season.name;
      this.currentEditingSeason = season;
      
      this.$nextTick(() => {
        this.$refs.seasonNameInput?.focus();
      });
    },
    
    async saveSeasonName(season) {
      try {
        if (this.editableSeasonName.trim() === '') {
          this.cancelEditSeason(season);
          return;
        }
        
        await this.updateSeason({
          uuid: season.uuid,
          name: this.editableSeasonName
        });
        
        this.editingSeason = {};
        this.currentEditingSeason = null;
        await this.fetchSeasons();
      } catch (error) {
        console.error('Error updating season name:', error);
      }
    },
    
    cancelEditSeason(season) {
      this.editingSeason = {};
      this.currentEditingSeason = null;
    },
    
    navigateToCard(cardUuid) {
      this.$router.push(`/card/${cardUuid}`);
    },
    
    updateUserAllowedStatus(isAllowed) {
      console.log('Received user allowed status:', isAllowed);
      this.isUserAllowed = isAllowed;
    },
    
    navigateToAddCard() {
      this.$router.push('/add-card');
    },
    
    async navigateToAddSeason() {
      try {
        const { createSeason } = await import('@/api');
        const newSeason = await createSeason();
        console.log('New season created:', newSeason);
        await this.fetchSeasons();
      } catch (error) {
        console.error('Error creating new season:', error);
        alert('Failed to create new season.');
      }
    },
    
    deleteSelectedCards() {
      // Ваша реализация удаления выбранных карточек
    }
  },
  mounted() {
    this.fetchSeasons();
  }
}
</script>

<style scoped>
.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: 1;
}

.background-logo {
  position: absolute;
  top: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  max-width: 250px;
  max-height: 250px;
  z-index: 1;
}

.separator-line {
  position: relative;
  margin-top: 370px;
  height: 2px;
  background-color: white;
  border: none;
  z-index: 2;
  width: 75%;
}

#seasons-container {
  position: relative;
  margin-top: 30px;
  z-index: 2;
  padding-bottom: 50px;
}

.error-message {
  text-align: center;
  margin: 50px 0;
  color: #ff5555;
}

.page-container {
  position: relative;
  min-height: 100vh;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 400px);
}

.season-wrapper {
  margin-bottom: 40px;
}

.season-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  position: relative;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.season-title {
  font-size: 24px;
  margin: 0;
  color: var(--accent-color);
  font-weight: 500;
  display: flex;
  align-items: center;
}

.edit-icon {
  margin-left: 10px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.edit-icon:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
}

.edit-icon svg {
  width: 16px;
  height: 16px;
}

.edit-input {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 5px;
  width: auto;
  max-width: 80%;
  text-align: inherit;
}

.edit-input:focus {
  border-color: white;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
  outline: none;
}

.add-card-button {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  padding: 5px 0;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
  white-space: nowrap;
  font-family: var(--font-family-main);
}

.add-card-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-color);
  transition: width 0.3s ease;
}

.add-card-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
}

.add-card-button:hover::after {
  width: 100%;
}

.delete-selected-button {
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 1px;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  padding: 5px 0;
  position: relative;
  text-decoration: none;
  transition: color 0.3s ease;
  white-space: nowrap;
  font-family: var(--font-family-main);
  margin-left: 15px;
}

.delete-selected-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: red;
  transition: width 0.3s ease;
}

.delete-selected-button:hover {
  color: red;
  -webkit-text-stroke: 0.15px darkred;
}

.delete-selected-button:hover::after {
  width: 100%;
}

.add-season-footer {
  padding: 20px 0 80px;
  text-align: center;
}

.add-new-season-btn {
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: inline-flex;
  justify-content: center;
  align-items: center;
  color: var(--text-color);
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 60px;
  padding: 0 30px;
  border: 2px dashed #555;
  margin: 0 auto;
}

.add-new-season-btn:hover {
  transform: translateY(-5px);
  border-color: var(--accent-color);
  color: var(--accent-color);
}

@media (max-width: 768px) {
  .season-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .season-title {
    margin-bottom: 10px;
  }
  
  .edit-input {
    max-width: 100%;
  }
  
  .add-card-button,
  .delete-selected-button {
    margin: 5px 0;
  }
}
</style>