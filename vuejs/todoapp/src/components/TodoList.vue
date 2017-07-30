<template>
	<div id="todolist">
		<ul>
			<todo v-for="todo in todos"
				  v-bind:todo="todo"
				  v-bind:key="todo.id">
			</todo>
		</ul>
	</div>
</template>

<script>
import Todo from './Todo.vue'

export default {
	components: {
		Todo,
	},
	computed: {
		todos () {
			return this.$store.state.todos
		}
	}
}
</script>
