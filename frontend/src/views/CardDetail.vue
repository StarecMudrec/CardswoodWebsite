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
          <h3 class=description-h3>Description:</h3>
          <div class="card-description-overlay">
            <p>{{ card.description }}</p>
          </div>
        </div>
        <div class="card-main-content">
          <h1 ref="cardNameRef">{{ card.name }}</h1>

          <div class="card-info-columns">
            <div class="card-info-column">
              <h3>Category</h3>
              <p>{{ card.category }}</p>
            </div>
            <div class="card-info-column">
              <h3>Season</h3>
              <p>{{ seasonName }}</p>
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
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

export default {
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const card = ref({})
    const seasonName = ref('')
    const comments = ref([])
    const loading = ref(true)
    const error = ref(null)
    const imageError = ref(false)
    const cardNameRef = ref(null)
    const baseFontSize = 100 // Базовый размер шрифта

    const adjustFontSize = () => {
      if (!cardNameRef.value) return
      
      const container = cardNameRef.value.parentElement
      const textElement = cardNameRef.value
      
      // Сброс к базовому размеру
      textElement.style.fontSize = `${baseFontSize}px`
      
      // Получаем реальные размеры
      const containerWidth = container.offsetWidth
      const textWidth = textElement.scrollWidth
      
      // Если текст не помещается, уменьшаем шрифт
      if (textWidth > containerWidth) {
        const scaleFactor = containerWidth / textWidth
        const newSize = Math.max(20, Math.floor(baseFontSize * scaleFactor)) // Минимальный размер 20px
        textElement.style.fontSize = `${newSize}px`
      }
    }

    const loadData = async () => {
      try {
        loading.value = true
        card.value = await fetchCardInfo(props.uuid)
        
        const season = await fetchSeasonInfo(card.value.season_id)
        seasonName.value = season.name
        
        comments.value = await fetchComments(card.value.id)
        
        // Двойной nextTick для гарантии обновления DOM
        nextTick(() => {
          nextTick(() => {
            adjustFontSize()
          })
        })
      } catch (err) {
        error.value = err.message || 'Failed to load card details'
        console.error('Error loading card:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadData()
      window.addEventListener('resize', adjustFontSize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', adjustFontSize)
    })

    watch(() => props.uuid, (newUuid) => {
      loadData(newUuid)
    })

    return {
      card,
      seasonName,
      comments,
      loading,
      error,
      imageError,
      cardNameRef
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
  top: 105%; /* Position below the image */
  left: 0;
  width: 100%;
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
  margin-bottom: 17px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  transition: font-size 0.3s ease; /* Плавное изменение размера */
  line-height: 1.2; /* Убедитесь, что line-height адекватный */
  font-size: 100px; /* Базовый размер */
}

@media (max-width: 768px) {
  .card-main-content h1 {
    font-size: 60px; /* Меньший базовый размер для мобильных */
  }
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

.card-info-columns {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 20px;
  margin-top: 2%;
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

.description-h3 {
  position: absolute;
  top: 95%; /* Position below the image */
  left: 0;
  width: 100%;
  font-size: 25px;
  text-align: center;
  color: var(--accent-color);
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
