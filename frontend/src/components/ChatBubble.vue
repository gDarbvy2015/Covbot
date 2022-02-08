<template>
  <div :class="message.self ? 'self-message' : 'bot-message'">
    <template v-if="!message.loading">
      <span v-html="message.self ? message.message : convertMessage(message.message)"></span>
    </template>
    <template v-else>
      <div class="loading-dots"></div>
    </template>
  </div>
</template>

<script>
var showdown = require("showdown")
var converter = new showdown.Converter()

export default {
  name: "ChatBubble",
  props: ["message"],
  methods: {
    convertMessage(msg) {
      return converter.makeHtml(msg);
    }
  }
}
</script>

<style scoped>
.loading-dots{
  width: 50px;
  height: 24px;
  background: radial-gradient(circle closest-side, currentColor 90%, #0000) 0 50%,
  radial-gradient(circle closest-side, currentColor 90%, #0000) 50% 50%,
  radial-gradient(circle closest-side, currentColor 90%, #0000) 100% 50%;
  background-size: calc(100% / 3) 12px;
  background-repeat: no-repeat;
  animation: dots-animation 1s infinite linear;
}

@keyframes dots-animation {
  20% {
    background-position: 0 0, 50% 50%, 100% 50%
  }
  40% {
    background-position: 0 100%, 50% 0, 100% 50%
  }
  60% {
    background-position: 0 50%, 50% 100%, 100% 0
  }
  80% {
    background-position: 0 50%, 50% 50%, 100% 100%
  }
}

.bot-message {
  margin-right: auto;
  background-color: white;
}

.self-message {
  margin-left: auto;
  background-color: #19233B;
  color: white;
}

p, span {
  margin: 0;
}
</style>