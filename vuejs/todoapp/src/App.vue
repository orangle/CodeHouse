<template>
  <div id="app">
    <user-input></user-input>
    <todo-list></todo-list>
  </div>
</template>

<script>
import TodoList from './components/TodoList.vue'
import UserInput from './components/UserInput.vue'

export default {
  components: {
    UserInput,
    TodoList
  }
}
</script>
