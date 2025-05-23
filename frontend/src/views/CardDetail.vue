<template>
  <div>
    <div class="background-container"></div>
    <div class="card-detail-container">
      <div v-if="loading" class="loading">Loading card details...</div>
      <div v-else-if="error" class="error-message">Error loading card: {{ error }}</div>
      <div v-else class="card-detail">
        <div class="card-image-container">
          <img 
            v-if="card.img" 
            :src="`/card_imgs/${card.img}`" 
            :alt="card.name" 
            class="card-detail-image"
            @error="imageError = true"
          />
          <div v-else class="image-placeholder">No image available</div>
          <h3>Description</h3>
          <div class="card-description-overlay">
            <p>{{ card.description }}</p>
          </div>
        </div>

        <div class="card-main-content">
          <h1>{{ card.name }}</h1>

          <div class="card-info-columns">
            <div class="card-info-column">
              <h3>Category</h3>
              <p>{{ card.category }}</p>
            </div>
            <div class="card-info-column">
              <h3>Season</h3>
              <p>{{ seasonName }}</p>
            </div>
            <div class="card-info-column">

            </div>
          </div>

          <div v-if="comments.length === 0" class="no-comments">
            No comments yet
          </div>
          <div v-else class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment">
              <div class="comment-text">{{ comment.text }}</div>
              <div class="comment-meta">User #{{ comment.user_id }}</div>
            </div>
          </div>
          <div class="comments-section">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchCardInfo, fetchSeasonInfo, fetchComments } from '@/api'

export default {
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      card: {},
      seasonName: '',
      comments: [],
      loading: true,
      error: null,
      imageError: false
    }
  },
  async created() {
    try {
      this.loading = true
      this.card = await fetchCardInfo(this.uuid)
      
      // Fetch season name
      const season = await fetchSeasonInfo(this.card.season_id)
      this.seasonName = season.name
      
      // Fetch comments
      this.comments = await fetchComments(this.card.id)
    } catch (err) {
      this.error = err.message || 'Failed to load card details'
      console.error('Error loading card:', err)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px; /* Adjust height as needed */
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%; /* Position the vertical center 80% down from the top, center horizontally */
  z-index: -1; /* Ensure it's behind the content */
}

.card-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error-message {
  text-align: center;
  margin: 50px 0;
  font-size: 18px;
}

.error-message {
  color: #ff5555;
}

.card-detail {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  margin-top: 30px;
}

.card-image-container {
  position: relative;
}

.card-detail-image {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
  border-radius: 17px;
  border-width: 15px;
  border-color: var(--bg-color);
  border-style: solid;
  background-color: #1e1e1e;
}

.image-placeholder {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1e1e1e;
  color: #666;
  border-radius: 17px;
  border-width: 10px;
  border-color: var(--card-border-color);
}

.card-description-overlay {
  position: absolute;
  top: 100%; /* Position below the image */
  left: 0;
  width: 100%;
  padding-top: 20px; /* Add space below the image */
  color: var(--text-color);
}

.card-description-overlay p {
  font-size: 18px;
  line-height: 1.6;
  word-wrap: break-word; /* Ensure text wraps */
  overflow-wrap: break-word;
  text-align: center; /* Center the description text */
}

.card-main-content {
  color: var(--text-color);
}


.card-main-content h1 {
  font-size: 70px;
  margin-bottom: 15px;
  margin-top: 15%;
  color: var(--accent-color);
}

.card-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  color: #aaa;
}

.card-info-section {
  margin-bottom: 20px;
}

.card-info-column h3 {
  font-size: 25px;
  margin-bottom: 15px;
  color: var(--accent-color);
}

.card-info-column p {
  font-size: 20px;
  line-height: 1.6;
  word-wrap: break-word;
  overflow-wrap: break-word;
}


.card-info-column {
  flex: 1;
  padding: 0 10px;
  text-align: center;
}


 .comments-section h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: var(--accent-color);
}


.no-comments {
  color: #666;
  font-style: italic;
}

.comment {
  background-color: #1e1e1e;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.comment-text {
  margin-bottom: 8px;
}

.comment-meta {
  font-size: 14px;
  color: #aaa;
}

@media (max-width: 480px) {
  .card-detail {
    grid-template-columns: 1fr;
  }
  
  .card-detail-image, .image-placeholder {
    max-height: 400px;
    border-width: 10px;
  }
}
</style>
