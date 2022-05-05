<template>
  <div>
    <b-shell
        :banner="banner"
        :shell_input="send_to_terminal"
        :style="style"
        @shell_output="prompt"
        autofocus
    ></b-shell>
  </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import shell from './bot-shell.vue'

Vue.component("b-shell", shell);
Vue.use(shell);

export default {
  name: "Vue",
  data() {
    return {
      style: {
        width: "800px"
      },
      send_to_terminal: "",
      banner: {
        header: "AlbertoBot v0.0.1",
        subHeader: "",
        helpHeader: "Hello! What is your name?",
        emoji: {first: ""},
        sign: "> ",
      },
      prologue: "",
      bot_lines: ["Hello! What is your name"]
    };
  },
  methods: {
    prompt(query) {
      if (this.$children[0].history_.length == 1) {
        this.prologue = `When the user is asked their name, they reply: '${query}'.`;
      }
      var data = {
        bot_lines: this.bot_lines,
        user_lines: this.$children[0].history_,
        prologue: this.prologue,
        query: query,
      }
      axios.post("api/query", data)
          .then((response) => {
            console.log(response);
            var reply = response["data"]["reply"]
            this.send_to_terminal = reply;
            this.bot_lines.push(reply);
          })
          .catch((error) => {
            console.log(error);
            this.send_to_terminal = "Connection error. Please check the logs.";
          });
    }
  }
};
</script>

<style>
