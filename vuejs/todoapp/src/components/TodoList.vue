<template>
	<div id="todolist">
		<ul>
			<li v-for="todo in todos">
				<todo v-bind:todo="todo" v-bind:id="todo.id">
				</todo>
			</li>
		</ul>
	</div>
</template>

<script>
import Todo from './Todo.vue'

export default {
	components: {
		Todo,
	},
	data: function(){
		return {
			todos: [
				{text: 'learn vue'},
				{text: 'Do hard things'}
			]
		}
	}
}
</script>
