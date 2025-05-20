<template>
  <div class="card-detail-container">
    <div v-if="loading" class="loading">Loading card details...</div>
    <div v-else-if="error" class="error-message">Error loading card: {{ error }}</div>
    <div v-else-if="card.id" class="card-detail">
      <div class="card-image-container">
        <img 
          v-if="card.img" 
          :src="`/card_imgs/${card.img}`" 
          :alt="card.name" 
          class="card-detail-image"
          @error="imageError = true"
        />
        <div v-else class="image-placeholder">No image available</div>
      </div>
      
      <div class="card-info">
        <h1>{{ card.name }}</h1>
        <div class="card-meta">
          <span class="card-category">{{ card.category }}</span>
          <span class="card-season">Season: {{ seasonName }}</span>
        </div>
        
        <div class="card-description">
          <h3>Description</h3>
          <p>{{ card.description }}</p>
        </div>
        
        <div class="comments-section">
          <h3>Comments</h3>
          <div v-if="comments.length === 0" class="no-comments">
            No comments yet
          </div>
          <div v-else class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment">
              <div class="comment-text">{{ comment.text }}</div>
              <div class="comment-meta">User #{{ comment.user_id }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="not-found">
      Card not found.
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
    } else {
      // Card not found
      this.error = 'Card not found';
    } catch (err) {
      this.error = err.message || 'Failed to load card details'
      console.error('Error loading card:', err)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style>
/* Global styles from App.vue */
:root {
  --background-color: #1a1a1a;
  --text-color: #ffffff;
  --accent-color: #ff5555;
  --card-background: #2a2a2a;
  --border-color: #444;
}

.card-detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  color: var(--text-color);
}

.loading, .error-message {
  text-align: center;
  margin: 50px 0;
  font-size: 18px;
  color: var(--text-color);
}

.error-message {
  color: #ff5555;
}

.card-detail {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  margin-top: 30px;
  background-color: var(--card-background);
}

.card-image-container {
  position: relative;
}

.card-detail-image {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
  border-radius: 8px;
  background-color: var(--background-color);
}

.image-placeholder {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1e1e1e;
  color: var(--text-color);
  border-radius: 8px;
}

.card-info {
  color: var(--text-color);
}

.card-info h1 {
  font-size: 28px;
  margin-bottom: 15px;
  color: var(--accent-color);
}

.card-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  color: var(--text-color);
}

.card-description {
  margin-bottom: 40px;
}

.card-description h3 {
  font-size: 20px;
  margin-bottom: 15px;
  color: var(--accent-color);
}

.card-description p {
  line-height: 1.6;
}

.comments-section {
  margin-top: 40px;
}

.comments-section h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: var(--accent-color);
}

.no-comments {
  color: var(--text-color);
  font-style: italic;
}

.comment {
  background-color: var(--background-color);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.comment-text {
  margin-bottom: 8px;color: var(--text-color);
}

.comment-meta {
  font-size: 14px;
  color: #aaa;
}

@media (max-width: 768px) {
  .card-detail {
    grid-template-columns: 1fr;
  }
  
  .card-detail-image, .image-placeholder {
    max-height: 400px;
  }
}
</style>
