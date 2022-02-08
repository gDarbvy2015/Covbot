<template>
  <div class="container">
    <n-scrollbar ref="scrollbarRef">
        <div class="message-container" ref="messageContainer">
          <transition-group name="expand">
            <div v-for="message in messages" :key="message.message" class="message-bubble-container" :class="message.self ? 'own-message': 'bot-message'">
              <span v-html="message.self ? message.message : convertMessage(message.message)"></span>
            </div>
          </transition-group>
        </div>
    </n-scrollbar>
    <div class="message-compose-container">
      <n-input v-model:value="currentMessage" @keyup.enter="sendMessage" size="large" type="text" placeholder="Write something..." />
      <Icon size="35" color="black" @click="sendMessage" class="sendIcon">
        <Send />
      </Icon>
    </div>
  </div>
</template>

<script>
import { Send } from '@vicons/ionicons5'
import { Icon } from '@vicons/utils'

var showdown = require("showdown")
var converter = new showdown.Converter()

export default {
  name: "ChatComponent",
  components: {
    Icon,
    Send
  },
  data() {
    return {
      messages: [
        {id: 1, self: true, message: "Hey! How many cases have there been in Austria this today?"},
        {id: 2, self: false, message: "I'm afraid I don't have any data on COVID cases in Austria today, yet. :( Try " +
              "again a bit later."},
        {id: 3, self: true, message: "How many people have been vaccinated this week in Germany?"},
        {id: 4, self: false, message: "More than **500.000** people have been vaccinated this week in Germany."},
        {id: 4, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 5, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 6, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 7, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 8, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 9, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 10, self: false, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 11, self: false, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 12, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 14, self: false, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 15, self: false, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 16, self: false, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        {id: 17, self: true, message: "TEEEEEEEEEEEEEEEEEEEEEEEEEEEEST."},
        //{id: 12, self: false, message: "OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK."},
        ],
      currentMessage: null
    }
  },
  mounted() {
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
      console.log(this.$refs.messageContainer)
      this.$refs.scrollbarRef.scrollTo({top: this.$refs.messageContainer.scrollHeight})
    }
  }
}
</script>

<style>
  .message-compose-container {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    margin: 13px;
    padding: 10px;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.2);
  }

  .container {
    display: flex;
    flex-direction: column;
    background-color: #F2F6FC;
    border-radius: 12px;
    width: 100%;
  }

  .sendIcon {
    margin: 0 5px 0 5px;
    cursor: pointer;
  }

  .message-container {
    padding: 15px 15px 0 15px;
    overflow-y: auto;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .sendButton {
    border-radius: 10px;
  }

  .message-bubble-container {
    padding: 14px 17px 14px 17px;
    flex: 0 0 100%;
    border-radius: 20px;
    font-size: 18px;
    max-width: 45%;
    overflow-wrap: break-word;
    box-shadow: 0 0 10px 1px rgba(0, 0, 0, 0.2);
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .bot-message {
    margin-right: auto;
    background-color: white;
  }

  p, span {
    margin: 0;
  }

  .own-message {
    margin-left: auto;
    background-color: #19233B;
    color: white;
  }

  .expand-enter-active {
    animation: bounce-in 0.3s;
  }
  .expand-leave-active {
    animation: bounce-in 0.3s reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: scale(0);
    }
    100% {
      transform: scale(1);
    }
  }
</style>