<script>
export default {
    name: "NewTask",
    data() {
        return {
            'title': '',
            error: '',
            successMessage: '',  // Добавляем сообщение об успехе
            host: "http://localhost:5174"
        }
    },
    methods: {
        add() {
            this.error = '';
            this.successMessage = '';
            fetch(this.host + '/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'title': this.title,
                    'is_done': false
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`Ошибка HTTP: ${response.status}`);
                }
                return response.json()
            }).then(task => {
                this.$emit('taskAdded', task); // Эмиттим событие с новой задачей
                this.title = ''; // Очищаем поле ввода
                this.successMessage = 'Задача успешно добавлена!';
                 // Устанавливаем сообщение об успехе
            }).catch(error => {
                console.error("Error during fetch request:", error)
                this.error = 'Не удалось сохранить задачу.'
            })
        }
    }
}
</script>

<template>
    <div class="input-group mb-3 mt-3">
        <input type="text" class="form-control" placeholder="Задача..." aria-label="Задача..."
               aria-describedby="button-addon2" v-model="title">
        <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="add">Добавить</button>
    </div>
    <small class="form-text text-muted" style="color: red;">{{ error }}</small>
    <small class="form-text text-success">{{ successMessage }}</small> <!-- Выводим сообщение об успехе -->
</template>

<style scoped>

</style>