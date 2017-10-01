<template>
  <div id="main">
    <div class="row">
      <div class="col-12"><h2 class="text-center">AI Overlord</h2></div>
    </div>
    <user></user>
    <div class="row">
      <div class="col-12">
        <img src="http://127.0.0.1:50000/images/neural.jpg" class="rounded mx-auto d-block"
        alt="Responsive image" height="100">
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <img src="http://127.0.0.1:50000/images/image.jpg" class="rounded mx-auto d-block" alt="Responsive image"
        height="100">
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <button v-on:click="classify">topology</button>
        <button v-on:click="classify">trainNN/nnconfig</button>
        <button v-on:click="classify">data sets</button>
        <button v-on:click="classify">label data</button>
      </div>
    </div>
  </div>
</template>
<script>
import user from '@/components/user'

export default {
  name: 'main',
  data () {
    return {
      user_id: ""

    }
  },
  components: {
    user
  },
  methods: {
    classify: function (event) {
      user_id = "ss";

    }},

  }
  </script>
