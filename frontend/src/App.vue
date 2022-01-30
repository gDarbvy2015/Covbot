<template>
  <div class="wrapper">
    <chat-component></chat-component>
  </div>
</template>

<script>
import ChatComponent from './components/ChatComponent.vue'

export default {
  name: 'App',
  components: {
    ChatComponent
  }
}
</script>

<style>
#app {
  margin-top: 60px;
}

.wrapper {
  max-width: 50%;
  margin: auto;
}
</style>
