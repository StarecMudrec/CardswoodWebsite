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
              ✏️
            </span>
          </h2>
        </div>
        <Season 
          :season="season" 
          @card-clicked="navigateToCard"
        />
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
    }
  },
  mounted() {
    this.fetchSeasons();
  }
}
</script>

<style scoped>
.season-header {
  position: relative;
}

.edit-icon {
  margin-left: 10px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.edit-icon:hover {
  opacity: 1;
}

.edit-input {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 2px 5px;
  width: auto;
  max-width: 80%;
}

/* Остальные стили остаются без изменений */
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

.season-title {
  font-size: 24px;
  margin: 0;
  color: var(--accent-color);
  font-weight: 500;
  display: flex;
  align-items: center;
}
</style>