<script>
export default {
    name: "Task",
    props: ['task'],
    data() {
        return {
            isEditing: false, // состояние редактирования
            editedTitle: this.task.title, // копия названия для редактирования
            host: "http://localhost:5174",
            error: null
        }
    },
    methods: {
      updateTaskStatus() {
        fetch(this.host + `/api/tasks/${this.task.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.task.title,
            is_done: this.task.is_done
          })
        }).then(response => {
            if (!response.ok) {
                 throw new Error(`Ошибка HTTP: ${response.status}`);
               }
            return response.json()
          }).then(updatedTask => {
             this.task.is_done = updatedTask.is_done
          }).catch(error => {
            console.error("Error during fetch request:", error)
            // если что-то пошло не так - показываем ошибку на экране
            this.error = 'Не удалось обновить задачу.';
          })
      },
      enableEditMode() {
          this.isEditing = true;
          this.editedTitle = this.task.title; // копируем текущий title для редактирования
      },
      saveTaskTitle() {
         fetch(this.host + `/api/tasks/${this.task.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: this.editedTitle, // отправляем измененный title
                    is_done: this.task.is_done
                })
            }).then(response => {
                if (!response.ok) {
                     throw new Error(`Ошибка HTTP: ${response.status}`);
                   }
                return response.json()
             }).then(updatedTask => {
                 this.task.title = updatedTask.title; // обновляем отображение
                 this.isEditing = false; // выходим из режима редактирования
               }).catch(error => {
                   console.error("Error during update title request:", error)
                   this.error = 'Не удалось обновить название задачи.';
                   this.isEditing = false;
               })
      },
       deleteTask() {
          fetch(this.host + `/api/tasks/${this.task.id}`, {
              method: 'DELETE'
          }).then(response => {
              if (!response.ok) {
                  throw new Error(`Ошибка HTTP: ${response.status}`);
              }
              this.$emit('taskDeleted', this.task.id);
          }).catch(error => {
            console.error("Error during delete request:", error)
            // если что-то пошло не так - показываем ошибку на экране
            this.error = 'Не удалось удалить задачу.'
          })
      }
    }
}
</script>

<template>
    <li class="list-group-item d-flex align-items-center" :class="{'list-group-item-success': task.is_done}">
       <input class="me-2" type="checkbox" v-model="task.is_done" @change="updateTaskStatus" />
        <span v-if="!isEditing" @dblclick="enableEditMode">
          {{ task.title }}
        </span>
        <input v-else type="text" class="form-control form-control-sm" v-model="editedTitle" @blur="saveTaskTitle" @keyup.enter="saveTaskTitle" style="width: auto; margin-right: 5px;">
        <button class="btn btn-sm btn-danger ms-auto" @click="deleteTask">
           <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
              <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
              <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H10a1 1 0 0 1 1 1v1h3.5a1 1 0 0 1 1 1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
            </svg>
         </button>
    </li>
</template>

<style scoped>

</style>