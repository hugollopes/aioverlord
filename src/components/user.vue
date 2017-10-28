<template>
  <div class="row">
    <div class="container">
    <div class="row">
      <div class="col-xs-12 panel" id="userId">{{userId}}</div>
    </div>
    <div class="row">
      <div class="col-xs-3 panel" id="creditsLabel">Credits: </div>
      <div class="col-xs-3 panel panel2" id="credits">{{credits}}</div>
      <div class="col-xs-3 panel" id="neuronsLabel">Neurons:</div>
      <div class="col-xs-3 panel panel2" id="neurons">{{neurons}}</div>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'user',
  props: {
    userId: {
      type: String,
      required: false,
      default: 'default',
    },
  },
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
    this.run();
  },
  methods: {
    run() {
      const self = this;
      this.intervalid1 = setInterval(() => {
        self.$log.debug(process.env.API_URL);
        axios.get(`${process.env.API_URL}/getuser`)
        .then((response) => {
          self.credits = response.data.credits;
          self.neurons = response.data.neurons;
        });
      }, 1000);
    },
  },
};
</script>


<style scoped>
.panel  {

  background-color: #2284a1;
      margin-bottom: 0px;
}
.panel2  {
  background-color: green;
      margin-bottom: 0px;
}



</style>
