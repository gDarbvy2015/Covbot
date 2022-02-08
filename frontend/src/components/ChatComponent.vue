<template>
  <div class="container">
    <n-space vertical class="message-container" ref="messageContainer">
      <div v-for="message in messages" :key="message.message" class="message-bubble-container" :class="message.self ? 'own-message': 'bot-message'">
        <span v-html="message.self ? message.message : convertMessage(message.message)"></span>
      </div>
    </n-space>
    <div class="message-compose-container">
      <n-input v-model:value="currentMessage" @keyup.enter="sendMessage" size="large" type="text" placeholder="Write something..." />
      <n-button type="info" size="large" @click="sendMessage">Send</n-button>
    </div>
  </div>
</template>

<script>

var showdown = require("showdown")
var converter = new showdown.Converter()

export default {
  name: "ChatComponent",
  data() {
    return {
      messages: [
        {id: 1, self: true, message: "Hey! How many cases have there been in Austria this today?"},
        {id: 2, self: false, message: "I'm afraid I don't have any data on COVID cases in Austria today, yet. :( Try " +
              "again a bit later."},
        {id: 3, self: true, message: "How many people have been vaccinated this week in Germany?"},
        {id: 3, self: false, message: "More than **500.000** people have been vaccinated this week in Germany."}
      ],
      currentMessage: null
    }
  },
  mounted() {
    this.scrollChatToBottom();
  },
  methods: {
    convertMessage(msg) {
      return converter.makeHtml(msg);
    },
    sendMessage() {
      if(this.currentMessage != null && this.currentMessage.trim() !== "") {
        let id = this.messages.length;
        this.messages.push({id: id, self: true, message: this.currentMessage});
        this.currentMessage = null;

        this.$nextTick(this.scrollChatToBottom);
      }
    },
    scrollChatToBottom() {
      this.$refs.messageContainer.$el.scrollTop = this.$refs.messageContainer.$el.scrollHeight;
    }
  }
}
</script>

<style>
  .message-compose-container {
    display: flex;
    gap: 10px;
  }

  .container {
    display: flex;
    flex-direction: column;
    row-gap: 20px;
    width: 100%;
  }

  .message-container {
    overflow-y: auto;
    height: 100%;
  }

  .message-bubble-container {
    padding: 9px;
    border-radius: 20px;
    font-size: 18px;
    display: inline-block;
    max-width: 45%;
    overflow-wrap: break-word;
  }

  .bot-message {
    float: left;
    background-color: #3096bf;
  }

  p, span {
    margin: 0;
  }

  .own-message {
    float: right;
    background-color: #57c441;
  }
</style>