<template>
  <GetWeather/>
</template>

<script>
import GetWeather from './components/GetWeather.vue'

export default {
  name: 'App',
  components: {
    GetWeather
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
