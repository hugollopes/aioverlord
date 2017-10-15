<template>

  <div class="row">
    <div class="col-6 col-sm-3">Cash</div>
    <div class="col-6 col-sm-3">{{credits}}</div>
    <div class="col-6 col-sm-3">Neurons</div>
    <div class="col-6 col-sm-3">4757663</div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'user',
  data () {
    return {
      name: "",
      credits: 1,
    }
  },
  created: function(){
  console.log(process.env.API_URL);
    axios.get(process.env.API_URL + "/getuser")
    .then(response => {this.name = response.data.name;
      this.credits = response.data.cash})
    }
  }
  </script>
