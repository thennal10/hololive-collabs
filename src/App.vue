<template>
  <NetworkContainer :collabLimit="collabLimit" :shadow="shadow"/>
  <Filters v-model:collabLimit="collabLimit" />
</template>

<script>
import NetworkContainer from './components/NetworkContainer'
import Filters from './components/Filters'

export default {
  name: 'App',
  components: {
    NetworkContainer,
    Filters
  },
  data() {
    return {
      collabLimit: 10
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
html, body, #app {
  font-family: 'Roboto', sans-serif;
  height: 100%;
  width: 100%;
  margin: 0;
}
</style>
