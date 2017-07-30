// store.js

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex) // only required if you're using modules.
              // We're using modules, so there you go.

const store = new Vuex.Store({
  state: {
    todos: [
      { text: 'Learn Vue.' },
      { text: 'Do hard things.' }
    ]
  },
  mutations: {
    'ADD_TODO': function (state, todo) {
      state.todos.push(todo)
    },
    'CLEAR_TODOS': function (state) {
      const todos = state.todos
      todos.splice(0, todos.length)
    }
  },
  actions: {
    addTodo (store, todo) {
      store.commit('ADD_TODO', todo)
    },
    clearTodos (store) {
      store.commit('CLEAR_TODOS')
    }
  }
})

export default store
