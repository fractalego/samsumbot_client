<template>
  <b-container>
    <Shell/>
  </b-container>
</template>

<script>
import Shell from './components/Shell.vue'

export default {
  name: 'App',
  components: {
    Shell
  }
}
</script>

<style>
body, html {
  padding: 0;
  margin: 0;
  width: 100%;
}
body {
  background-color: black;
}
</style>