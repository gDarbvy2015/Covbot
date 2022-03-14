<template>
  <n-dialog-provider>
    <div class="wrapper">
      <chat-window></chat-window>
    </div>
  </n-dialog-provider>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue'

export default {
  name: 'App',
  components: {
    ChatWindow
  }
}
</script>

<style>
.wrapper {
  margin: auto;
  max-height: 100vh;
  display: flex;
}

@media only screen and (min-width: 750px) {
  .wrapper {
    max-width: 75%;
  }
}

@media only screen and (min-width: 1300px) {
  .wrapper {
    max-width: 65%;
  }
}


html {
  height: 100vh;
}

body {
  height: 100vh;
}

#app, .wrapper {
  height: 100%;
}
</style>
