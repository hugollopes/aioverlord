<template>
  <div class="row">
    <div class="col-xs-3 panel" id="creditsLabel">Credits: </div>
    <div class="col-xs-3 panel panel2" id="credits">{{credits}}</div>
    <div class="col-xs-3 panel" id="neuronsLabel">Neurons:</div>
    <div class="col-xs-3 panel panel2" id="neurons">{{neurons}}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'user',
  data() {
    return {
      name: '',
      credits: 0,
      neurons: 0,
    };
  },
  mounted() {
    this.$log.debug(process.env.API_URL);
    axios.get(`${process.env.API_URL}/getuser`)
    .then((response) => {
      this.name = response.data.name;
      this.credits = response.data.credits;
      this.neurons = response.data.neurons;
    });
  },
};
</script>


<style scoped>
.panel  {

  background-color: #2284a1;
}
.panel2  {
  background-color: green;
}



</style>
