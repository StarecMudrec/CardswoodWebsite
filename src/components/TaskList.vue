<script>
import Task from "@/components/Task.vue";
import NewTask from "@/components/NewTask.vue";

export default {
    name: "TaskList",
    components: {NewTask, Task},
    data() {
        return {
            tasks: [],
            host: "http://localhost:5174"
        }
    },
  methods: {
      handleTaskAdded(task) {
          this.tasks.push(task)
      },
      handleTaskDeleted(taskId) {
        this.tasks = this.tasks.filter(task => task.id !== taskId);
      }
    },
        // mounted срабатывает при загрузке страницы
        mounted() {
            console.log("running")
            // отправляем запрос на получение списка всех задач с сервера
            fetch(this.host + '/api/tasks').then(response => response.json()).then(tasks => {
                // полученный список задач с сервера кладем в реактивную переменную tasks (он покажется на экране)
                this.tasks = tasks;
            }).catch(error => {
                // если что-то пошло не так - показываем ошибку
                this.error = 'Не удалось загрузить список задач с сервера';
            });
        }
}
</script>

<template>
    <div class="container mt-4">
        <ul class="list-group">
            <Task v-for="task in tasks" :key="task.id" :task="task" @taskDeleted="handleTaskDeleted"></Task>
        </ul>
        <NewTask @taskAdded="handleTaskAdded"></NewTask>
    </div>
</template>

<style scoped>

</style>