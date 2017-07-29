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
			console.log(this.newTodoText, 'create!')
		},
		clearTodos () {
			console.log('Todos cleared!')
		}
	}
}
</script>
