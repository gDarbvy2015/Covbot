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
.wrapper {
  max-width: 75%;
  margin: auto;
  max-height: 100vh;
  display: flex;
}

html{
  height: 100vh;
}

body {
  height: calc(100vh - 2*15px);
  padding: 15px 0 15px 0;
}

#app, .wrapper {
  height: 100%;
}
</style>
