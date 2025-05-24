<template>
  <div class="add-card">
    <h2>Add New Card</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Card Name:</label>
        <input type="text" id="name" v-model="card.name" required>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="card.description" required></textarea>
      </div>
      <div class="form-group">
        <label for="category">Category:</label>
        <input type="text" id="category" v-model="card.category" required>
      </div>
      <div class="form-group">
        <label for="season">Season:</label>
        <input type="number" id="season" v-model="card.season" required>
      </div>
      <div class="form-group">
        <label for="image">Card Image:</label>
        <input type="file" id="image" @change="handleFileUpload" accept="image/*" required>
      </div>
      <button type="submit">Add Card</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      card: {
        name: '',
        description: '',
        category: '',
        season: null,
        image: null
      }
    };
  },
  methods: {
    handleFileUpload(event) {
      this.card.image = event.target.files[0];
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('name', this.card.name);
      formData.append('description', this.card.description);
      formData.append('category', this.card.category);
      formData.append('season', this.card.season);
      formData.append('image', this.card.image);

      try {
        // Adjust the URL based on your backend endpoint for adding cards
        const response = await axios.post('/api/add-card', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Card added successfully:', response.data);
        // Optionally, clear the form or redirect the user
        this.resetForm();
      } catch (error) {
        console.error('Error adding card:', error);
      }
    },
    resetForm() {
      this.card = {
        name: '',
        description: '',
        category: '',
        season: null,
        image: null
      };
      // Clear the file input separately
      const fileInput = document.getElementById('image');
      if (fileInput) {
        fileInput.value = '';
      }
    }
  }
};
</script>

<style scoped>
.add-card {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>