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
        </div>
        
        <div class="card-content-wrapper">
          <!-- Название карточки и главная разделительная линия -->
          <div class="card-header-section">
            <div class="title-container">
              <h1 ref="cardNameRef">{{ card.name }}</h1>
            </div>
            <div class="main-divider"></div>
          </div>
          
          <!-- Описание карточки -->
          <div class="card-description-section">
            <div class="card-description">
              <p>{{ card.description }}</p>
            </div>
            <div class="secondary-divider"></div>
          </div>
          
          <!-- Информация о категории и сезоне -->
          <div class="card-info-section">
            <div class="card-info-columns">
              <div class="card-info-column">
                <h3>Category:</h3>
                <p>{{ card.category }}</p>
              </div>
              <div class="card-info-column">
                <h3>Season:</h3>
                <p>{{ seasonName }}</p>
              </div>
            </div>
          </div>
          
          <!-- Комментарии -->
          <div class="comments-section">
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

    const checkTitleLength = () => {
      nextTick(() => {
        if (!cardNameRef.value || window.innerWidth > 768) return;
        
        const element = cardNameRef.value;
        const container = element.parentElement;
        element.classList.remove('long-title');
        
        // Check if text overflows
        if (element.scrollWidth > container.offsetWidth * 1.1) {
          element.classList.add('long-title');
        }
      });
    };

    const adjustFontSize = () => {
      nextTick().then(() => {
        if (!cardNameRef.value) return
        
        const element = cardNameRef.value
        const container = element.parentElement
        isMobile.value = window.innerWidth <= 768;
        
        if (!isMobile.value) {
          // Сброс стилей
          element.style.fontSize = '';
          element.style.whiteSpace = 'nowrap';
          element.style.lineHeight = '1.1';
          
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
          return;
        }
        // Мобильная логика
        const containerWidth = container.offsetWidth;
        let fontSize = 42; // Стартовый размер для мобильных
        const minFontSize = 28; // Минимальный размер
        
        // Проверяем, помещается ли текст
        element.style.fontSize = `${fontSize}px`;
        
        while (element.scrollWidth > containerWidth && fontSize > minFontSize) {
          fontSize -= 1;
          element.style.fontSize = `${fontSize}px`;
        }

        // Если достигли минимума и всё ещё не влезает - разрешаем перенос
        if (element.scrollWidth > containerWidth && fontSize <= minFontSize) {
          element.style.whiteSpace = 'normal';
          element.style.lineHeight = '1.2';
        }
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
      window.addEventListener('resize', adjustFontSize);
      adjustFontSize();
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
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
  border: 15px solid var(--bg-color);
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
  border: 10px solid var(--card-border-color);
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
}

/* Исправленная секция заголовка */
.card-header-section {
  /* Keep existing styles */
  margin-top: 64px; /* Add top margin to push content down (adjust value as needed) */
  /* Add other styling for spacing or alignment */
  position: relative;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.title-container {
  position: absolute;
  bottom: 17px; /* Расстояние до разделителя */
  width: 100%;
}

.card-header-section h1 {
  margin: 0;
  padding: 0;
  white-space: nowrap;
  font-size: 100px;
  line-height: 1;
  color: var(--text-color);
  display: inline-block;
  vertical-align: bottom;
  transform-origin: left bottom;
  transition: font-size 0.2s ease;
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
}

.main-divider {
  height: 2px;
  width: 100%;
  background-color: var(--card-border-color);
  margin: 0; /* Убираем margin */
  position: absolute; /* Абсолютное позиционирование */
  bottom: -20px; /* Позиционируем ниже текста */
}

/* Остальные стили без изменений */
.card-description-section {
  padding: 30px 0;
}

.card-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-color);
  text-align: center; 
}

.secondary-divider {
  height: 1px;
  width: 100%;
  background-color: var(--card-border-color);
  margin-top: 30px;
}

.card-info-section {
  padding: /*2*/0px 0;
}

.card-info-columns {
  display: flex;
  justify-content: space-around;
}

.card-info-column {
  flex: 1;
  text-align: center;
}

.card-info-column h3 {
  font-size: 25px;
  margin-bottom: 10px;
  color: var(--accent-color);
}

.card-info-column p {
  font-size: 20px;
  line-height: 1.6;
  color: var(--text-color);
}

.comments-section {
  margin-top: auto;
  padding-top: 40px;
  text-align: center;
}

.no-comments {
  color: #666;
  font-style: italic;
}

.comments-list {
  max-width: 800px;
  margin: 0 auto;
}

.comment {
  background-color: #1e1e1e;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  text-align: left;
}

.comment-text {
  margin-bottom: 8px;
  color: var(--text-color);
}

.comment-meta {
  font-size: 14px;
  color: #aaa;
}

/* Mobile-specific fixes */
@media (max-width: 768px) {
  .card-detail {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .card-header-section {
    position: relative;
    min-height: auto;
    margin: 20px 0 10px 0;
    padding: 0 15px;
  }

  .title-container {
    position: static;
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .card-header-section h1 {
    font-size: min(9vw, 42px); /* Dynamic scaling with max size */
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
    text-align: center;
    padding: 0;
    margin: 0 0 15px 0;
    display: inline;
    transition: font-size 0.3s ease;
  }

  .main-divider {
    position: static;
    margin: 10px 0;
  }

  /* Additional scaling for very long titles */
  .card-header-section h1.long-title {
    font-size: min(7vw, 36px);
    line-height: 1.3;
  }
}
</style>