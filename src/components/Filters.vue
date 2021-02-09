<template>
    <div>
        <span>Minimum Collab Filter:</span><br>
        <input type="range" min="0" max="20" 
        :value="collabLimit" @input="$emit('update:collabLimit', Number($event.target.value))">
        <br>
        <a href="github link">What is this?</a>
    </div>
</template>

<script>
export default {
  name: 'Filters',
  props: {
    collabLimit: Number
  }
}
</script>

<style scoped>
div {
  font-family: Roboto;
  position: fixed;
  top: 10px;
  left: 10px;

  background-color: white;
  padding: 10px;
  border-radius: 3px;
}

a {
  font-size: 0.9rem;
  color: grey;
  text-align: center;
  width: 100%;
  display: block;
}

</style>
