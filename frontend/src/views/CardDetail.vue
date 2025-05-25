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
            @dblclick="handleImageDoubleClick"
          />
          <!-- <button v-if="isUserAllowed" class="replace-image-button">Replace Image</button> -->
          <div v-else class="image-placeholder">No image available</div>
        </div>
        
        <div class="card-content-wrapper">
          <!-- Название карточки и главная разделительная линия -->
          <div class="card-header-section">
            <div class="title-container">
              <h1 ref="cardNameRef">
                
                <span v-if="!editing.name">{{ card.name }}</span>
                <input 
                  v-else
                  v-model="editableCard.name"
                  @blur="saveField('name')"
                  @keyup.enter="saveField('name')"
                  ref="nameInput"
                  class="edit-input"
                  maxlength="100"
                >
                <span v-if="isUserAllowed" class="edit-icon" @click="startEditing('name')">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </span>
              </h1>
            </div>
            <div v-if="nameError" class="error-message">{{ nameError }}</div>
            <div class="main-divider"></div>
          </div>
          
          <!-- Описание карточки -->
          <div class="card-description-section">
            <div class="card-description">
              <p v-if="!editing.description">{{ card.description }}</p>
              <textarea
                v-else
                v-model="editableCard.description"
                @blur="saveField('description')"
                @keyup.enter="saveField('description')"
                ref="descriptionInput"
                maxlength="1000"
                class="edit-textarea"
              ></textarea>
              <span v-if="isUserAllowed" class="edit-icon" @click="startEditing('description')">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </span>
            </div>
            <div v-if="descriptionError" class="error-message">{{ descriptionError }}</div>
            <div class="secondary-divider"></div>
          </div>
          
          <!-- Информация о категории и сезоне -->
          <div class="card-info-section">
            <div class="card-info-columns">
              <div class="card-info-column">
                <h3>
                  Category:
                  <span v-if="isUserAllowed" class="edit-icon" @click.stop="toggleEdit('category')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </span>
                </h3>
                <div class="category-container">
                  <p v-if="!editing.category">{{ card.category }}</p>
                  <input
                    v-else
                    v-model="editableCard.category"
                    @blur="saveField('category')"
                    @keyup.enter="saveField('category')"
                    @keyup.esc="cancelEdit('category')"
                    ref="categoryInput"
                    class="edit-input"
                    maxlength="20"
                  >
                </div>
                <div v-if="categoryError" class="error-message">{{ categoryError }}</div>
              </div>
              <div class="card-info-column">
                <h3>
                  Season:
                  <span v-if="isUserAllowed" class="edit-icon" @click.stop="toggleEdit('season')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </span>
                </h3>
                <div v-if="!isUserAllowed">
                  <p>{{ seasonName }}</p>
                </div>
                <select
                  v-else
                  v-if="isUserAllowed" 
                  v-model="editableCard.season_uuid"
                  @change="saveField('season')"
                  @blur="cancelEdit('season')"
                  ref="seasonInput"
                  class="edit-input-select"
                >
                  <option class="edit-input-option" v-for="season in allSeasons" :key="season.uuid" :value="season.uuid">
                    {{ season.name }}
                  </option>
                </select>
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
    <div v-if="saveError" class="error-message">{{ saveError }}</div>
  <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none;">
  </div>
</template>

<script>
import { fetchCardInfo, fetchSeasonInfo, fetchComments, checkUserPermission, fetchUserInfo, fetchSeasons } from '@/api'
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

export default {
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const fileInput = ref(null)
    // Refs для полей ввода
    const nameInput = ref(null)
    const descriptionInput = ref(null)
    const categoryInput = ref(null)
    const seasonInput = ref(null)

    const card = ref({})
    const editableCard = ref({})
    const seasonName = ref('')
    const allSeasons = ref([])
    const comments = ref([])
    const loading = ref(true)
    const error = ref(null)
    const imageError = ref(false)
    const saveError = ref(null); // New ref for save errors
    const nameError = ref(null); // New ref for name errors
    const descriptionError = ref(null); // New ref for description errors
    const categoryError = ref(null); // New ref for category errors
    const cardNameRef = ref(null)
    const isUserAllowed = ref(false)
    const editing = ref({
      name: false,
      description: false,
      category: false,
      season: false
    })

    const adjustFontSize = () => {
      nextTick(() => {
        if (!cardNameRef.value) return;
        
        const element = cardNameRef.value;
        const container = element.parentElement;
        
        // Сброс стилей
        element.style.fontSize = '';
        element.style.whiteSpace = 'nowrap';
        
        const containerWidth = container.clientWidth;
        let fontSize = 100; // Начальный размер
        
        // Устанавливаем начальный размер
        element.style.fontSize = `${fontSize}px`;
        void element.offsetWidth; // Принудительный рефлоу
        
        // Если текст не помещается - вычисляем оптимальный размер
        if (element.scrollWidth > containerWidth) {
          const ratio = containerWidth / element.scrollWidth;
          fontSize = Math.max(
            28,
            Math.min(
              fontSize, 
              Math.floor(fontSize * ratio * 0.85)
            )
          );
          element.style.fontSize = `${fontSize}px`;
          
          if (element.scrollWidth > containerWidth * 1.05) {
            element.style.whiteSpace = 'normal';
            element.style.lineHeight = '1.2';
          }
        }
      });
    };
    

    const toggleEdit = (field) => {
      if (editing.value[field]) {
        cancelEdit(field)
      } else {
        startEditing(field)
      }
    }

    const cancelEdit = (field) => {
      editing.value = { ...editing.value, [field]: false }
    }


    const startEditing = (field) => {
      editing.value = { ...editing.value, [field]: true }
      editableCard.value = { ...card.value }
      
      nextTick(() => {
        switch(field) {
          case 'name':
            nameInput.value?.focus()
            nameInput.value?.select()
            break
          case 'category':
            categoryInput.value?.focus()
            categoryInput.value?.select()
            break;
          case 'description':
            descriptionInput.value?.focus()
            break
          case 'category':
            categoryInput.value?.focus()
            break
        }
      })
    }

    const saveField = async (field) => {
      saveError.value = null; // Clear previous save errors
      try {
        // console.log('Saving field:', field, 'with data:', editableCard.value);

        let dataToSend = {};
        
        // Особый случай для сезона
        if (field === 'season') {
          dataToSend = {
            season_uuid: editableCard.value.season_uuid
          };
        } else if (field === 'category') {
            // Проверка длины для категории перед сохранением
            if (editableCard.value.category && editableCard.value.category.length > 20) {
                categoryError.value = 'Category cannot exceed 20 characters.';
                throw new Error('Validation failed on frontend.'); // Prevent saving if validation fails
            }
             dataToSend = { [field]: editableCard.value[field] };
        } else {
          dataToSend = {
            [field]: editableCard.value[field]
          };
        }

        const response = await fetch(`/api/cards/${card.value.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          },
          body: JSON.stringify(dataToSend)
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to update card');
        }

        // Обновляем локальные данные
        if (field === 'season') {
          const season = allSeasons.value.find(s => s.uuid === editableCard.value.season_uuid);
          seasonName.value = season?.name || '';
          card.value.season_uuid = editableCard.value.season_uuid;
        } else {
          card.value[field] = editableCard.value[field];
        }

        editing.value = { ...editing.value, [field]: false };
      } catch (err) {
        console.error('Error updating card:', err);
        saveError.value = err.message || 'Failed to update card'; // Set save error
      }
    }

    const handleImageDoubleClick = () => {
      if (isUserAllowed.value && fileInput.value) {
        fileInput.value.click();
      }
    };

    const handleFileChange = async (event) => {
      const file = event.target.files[0];
      if (!file || !isUserAllowed.value) {
        return;
      }

      const formData = new FormData();
      formData.append('image', file);

      try {
        const response = await fetch(`/api/cards/${card.value.uuid}/image`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          },
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to upload image');
        }

        // Optionally refresh the card data to show the new image
        loadData();
      } catch (err) {
        console.error('Error uploading image:', err);
      }
    };
    const loadData = async () => {
      try {
        loading.value = true;
        
        // Загружаем карточку
        card.value = await fetchCardInfo(props.uuid);
        editableCard.value = { ...card.value };
        
        // Загружаем сезоны
        const seasons = await fetchSeasons();
        allSeasons.value = seasons.map(season => ({
          uuid: season.uuid,
          name: season.name
        }));
        
        // Загружаем текущий сезон
        if (card.value.season_id) {
          const season = await fetchSeasonInfo(card.value.season_id);
          seasonName.value = season.name;
          editableCard.value.season_uuid = season.uuid;
        }
        
        // Загружаем комментарии
        comments.value = await fetchComments(card.value.id)
        
        // Проверяем права пользователя
        try {
          const userInfo = await fetchUserInfo()
          if (userInfo?.username) {
            const permissionResponse = await checkUserPermission(userInfo.username)
            isUserAllowed.value = permissionResponse.is_allowed
          }
        } catch (authError) {
          console.log('User not authenticated, editing disabled')
          isUserAllowed.value = false
        }
        
        setTimeout(adjustFontSize, 0)
      } catch (err) {
        error.value = err.message || 'Failed to load card details'
        console.error('Error loading card:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      window.addEventListener('resize', adjustFontSize)
      loadData()
    })

    onUnmounted(() => {
      window.removeEventListener('resize', adjustFontSize)
    })

    watch(() => props.uuid, loadData)

    watch(() => editableCard.value.name, (newName) => {
      if (newName && newName.length > 100) {
        nameError.value = 'Name cannot exceed 100 characters.';
      } else {
        nameError.value = null;
      }
    });

    watch(() => editableCard.value.description, (newDescription) => {
      if (newDescription && newDescription.length > 1000) {
        descriptionError.value = 'Description cannot exceed 1000 characters.';
      } else {
        descriptionError.value = null;
      }
    });

    watch(() => editableCard.value.category, (newCategory) => {
      if (newCategory && newCategory.length > 20) {
        categoryError.value = 'Category cannot exceed 20 characters.';
      } else {
        categoryError.value = null;
      }
    });

    return {
      card,
      editableCard,
      seasonName,
      categoryError, // Return categoryError
      allSeasons,
      comments,
      loading,
      error,
      nameError, // Return nameError
      descriptionError, // Return descriptionError
      saveError, // Return saveError
      imageError,
      cardNameRef,
      editing,
      isUserAllowed,
      nameInput,
      descriptionInput,
      categoryInput,
      seasonInput,
      fileInput,
      handleImageDoubleClick,
      handleFileChange,
      startEditing,
      saveField,
      toggleEdit,
      cancelEdit,
      fileInput,
      handleImageDoubleClick,
      handleFileChange
    }
  }
}
</script>

<style scoped>
/* Существующие стили остаются без изменений */
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

.category-container {
  background: none;
  padding: 12px 20px;
  border-radius: 8px;
  margin-top: 8px;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  text-align: center;
}
.category-container p {
  color: white;
  font-size: 20px;
  margin: 0;
  word-break: break-word;
  text-align: center;
}


/* Стили для полей ввода при редактировании */
.edit-input {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 5px;
  width: 80%;
  text-align: inherit;
  transition: inherit;
  text-shadow: inherit;
  letter-spacing: inherit;
}
.edit-input:focus {
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
}

.edit-input-select {
  width: 50%;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: white;
  font-size: 20px;
  text-align: center; 
  cursor: pointer;
  appearance: none; /* Remove default dropdown arrow */
  margin-top: 6px;
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2020%2020%22%20fill%3D%22none%22%20stroke%3D%22%23ffffff%22%20stroke-width%3D%222%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpolyline%20points%3D%226%209%2012%2015%2018%209%22%2F%3E%3C%2Fsvg%3E'); /* Custom dropdown arrow */
  background-repeat: no-repeat;
  background-position: right 15px center;
  background-size: 1em;
  font-family: inherit;
}

.edit-input-select option { 
  color: inherit;
  background: var(--bg-color);
}

.edit-textarea {
  font-size: inherit;
  font-family: inherit;
  color: inherit;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--accent-color);
  border-radius: 4px;
  padding: 10px;
  width: 100%;
  min-height: 100px;
  resize: vertical;
}

.edit-input-select:focus {
  outline: none;
  box-shadow: none;
  background-color: transparent;
}

.replace-image-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: var(--bg-color);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 26px;
  font-family: var(--font-family-main);
  font-weight: 500;
  transition: background-color 0.3s ease;
}

/* Остальные существующие стили без изменений */
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
  cursor: pointer; /* Add cursor pointer to indicate it's interactive */
}

.card-detail-image {
  width: 100%;
  max-height: 600px;
  object-fit: contain;
  border-radius: 17px;
  border: 10px solid var(--bg-color);
  background-color: #1e1e1e;
  cursor: pointer; /* Add cursor pointer to indicate it's interactive */
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
  border: 10px solid var(--bg-color);
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
}

.card-header-section {
  margin-top: 64px;
  position: relative;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.title-container {
  position: absolute;
  bottom: 17px;
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
  transition: color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.main-divider {
  height: 2px;
  width: 100%;
  background-color: var(--card-border-color);
  top: 20%;
  position: relative;
  bottom: -20px;
}

.card-description-section {
  padding: 30px 0;
}

.card-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-color);
  text-align: center; 
  position: relative;
}

.secondary-divider {
  height: 1px;
  width: 100%;
  background-color: var(--card-border-color);
  margin-top: 30px;
}

.card-info-section {
  padding: 0px 0;
}

.card-info-columns {
  display: flex;
  justify-content: space-around;
}

.card-info-column {
  flex: 1;
  text-align: center;
  position: relative;
}

.card-info-column h3 {
  font-size: 25px;
  margin-bottom: 10px;
  color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
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

@media (max-width: 768px) {
  .card-detail {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .card-header-section {
    text-align: center;
    margin-top: -10px;
    min-height: 57px;
  }

  .card-content-wrapper {
    padding: 0 15px;
  }
  .title-container {
    width: 100%;
    overflow: hidden;
    position: relative;
    bottom: auto;
  }

  .card-header-section h1 {
    font-size: 100px;
    line-height: 1.1;
    margin: 0;
    padding: 0;
    white-space: nowrap;
    transition: all 0.3s ease;
    word-break: break-word;
  }
  .card-header-section h1.force-wrap {
    white-space: normal;
    line-height: 1.3;
  }

  .main-divider {
    margin-top: 15px;
  }
  .card-description {
    position: relative;
    left: -5%;
    width: 110%;
  }

  .card-detail-image {
    border-radius: 15px;
    border: 10px solid var(--bg-color);
  }

  .edit-input {
    width: 100%;
  }
}
</style>