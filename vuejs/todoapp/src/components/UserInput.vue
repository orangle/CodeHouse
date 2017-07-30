<template>
	<div id="user-inputs">
		<input v-model="newTodoText" v-on:keyup.enter="createTodo">
		<button v-on:click="clearTodos">
			Clear
		</button>
	</div>
</template>

<script>
export default {
	data: function(){
		return {newTodoText: ''}
	},
	methods: {
		createTodo () {
			this.$store.dispatch('addTodo', {text: this.newTodoText})
			this.newTodoText = ''
		},
		clearTodos () {
			this.$store.dispatch('clearTodos')
		}
	}
}
</script>
