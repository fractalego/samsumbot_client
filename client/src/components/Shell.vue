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
        helpHeader: "> Hello! What is your name?",
        emoji: {first: ""},
        sign: "> ",
      },
    };
  },
  methods: {
    prompt(value) {
      if (value != "") {
        this.send_to_terminal = "> HELLO ALBERTO!\n";
      }
    }
  }
};
</script>

<style>
