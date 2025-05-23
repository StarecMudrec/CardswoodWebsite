<template>
  <div>
    <div class="background-container"></div>
    <div class="card-detail-container">
      <div v-if="loading" class="loading">Loading card details...</div>
      <div v-else-if="error" class="error-message">Error loading card: {{ error }}</div>
      <div v-else class="card-detail">
        <div class="card-image-container">
          <img 
            v-if="card.img && !imageError" 
            :src="`/card_imgs/${card.img}`" 
            :alt="card.name" 
            class="card-detail-image"
            @error="imageError = true"
          />
          <div v-else class="image-placeholder">No image available</div>
          <h3 class="description-h3">Description:</h3>
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

    const adjustFontSize = () => {
      nextTick().then(() => {
        if (!cardNameRef.value) return
        
        const element = cardNameRef.value
        const container = element.parentElement
        
        // Сброс стилей для чистых измерений
        element.style.fontSize = ''
        element.style.whiteSpace = 'nowrap'
        element.style.display = 'inline-block'
        
        // Получаем ширины
        const containerWidth = container.clientWidth
        let fontSize = 100 // Начальный размер
        
        // Устанавливаем начальный размер
        element.style.fontSize = `${fontSize}px`
        void element.offsetWidth // Принудительный рефлоу
        
        // Если текст не помещается - вычисляем оптимальный размер
        if (element.scrollWidth > containerWidth) {
          const ratio = containerWidth / element.scrollWidth
          fontSize = Math.floor(fontSize * ratio * 0.95) // 5% запаса
          fontSize = Math.max(20, fontSize) // Минимум 20px
          element.style.fontSize = `${fontSize}px`
        }
        
        // Восстанавливаем стандартное отображение
        element.style.display = ''
      })
    }

    const loadData = async () => {
      try {
        loading.value = true
        card.value = await fetchCardInfo(props.uuid)
        
        const season = await fetchSeasonInfo(card.value.season_id)
        seasonName.value = season.name
        
        comments.value = await fetchComments(card.value.id)
        
        // Вызываем после полного рендеринга
        setTimeout(adjustFontSize, 0)
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

    watch(() => props.uuid, loadData)

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
  height: 400px;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: -1;
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
  top: 105%;
  left: 0;
  width: 100%;
  color: var(--text-color);
}

.card-description-overlay p {
  font-size: 18px;
  line-height: 1.6;
  word-wrap: break-word;
  overflow-wrap: break-word;
  text-align: center;
}

.card-main-content {
  color: var(--text-color);
  width: 100%;
  overflow: hidden;
}

.card-main-content h1 {
  margin: 0 0 17px 0;
  padding: 0;
  white-space: nowrap;
  font-size: 100px;
  line-height: 1.2;
  transition: font-size 0.2s ease;
  will-change: font-size;
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
  top: 95%;
  left: 0;
  width: 100%;
  font-size: 25px;
  text-align: center;
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

@media (max-width: 768px) {
  .card-detail {
    grid-template-columns: 1fr;
  }
  
  .card-main-content h1 {
    font-size: 60px;
  }
  
  .card-detail-image, .image-placeholder {
    max-height: 400px;
    border-width: 10px;
  }
}
</style>