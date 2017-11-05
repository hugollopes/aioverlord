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
      default: '',
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
    this.run(this.userId);
  },
  methods: {
    run(userId, token) {
      const self = this;
      if (userId !== '') {
        this.intervalid1 = setInterval(() => {
          self.$log.debug(process.env.API_URL);
          const postdata = { username: userId,
            password: '',
            token,
          };
          axios.post(`${process.env.API_URL}/getuser`, postdata)
        .then((response) => {
          self.credits = response.data.credits;
          self.neurons = response.data.neurons;
        });
        }, 1000);
      }
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
