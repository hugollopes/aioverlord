<template>
  <div id="main">
    <div class="row">
      <div><h2 class="text-center">AI Overlord</h2></div>
    </div>
    <user></user>
    <classifier v-show="show_classify" ></classifier>
    <div class="row">
      <div class="col-12">
        <img src="../images/neural.jpg" class="rounded mx-auto d-block"
        alt="Responsive image" height="100">
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <img src="../images/image.jpg" class="rounded mx-auto d-block" alt="Responsive image"
        height="100">
      </div>
    </div>

    <div class="row">
      <div class="col-xs-12">
        <button v-on:click="classify">topology</button>
        <button v-on:click="classify">trainNN/nnconfig</button>
        <button v-on:click="classify">data sets</button>
        <button v-on:click="classify">label data</button>
      </div>
    </div>
    <fileupload></fileupload>
  </div>
</template>
<script>
import user from '@/components/user';
import classifier from '@/components/classifier';
import fileupload from '@/components/fileupload';


export default {
  name: 'main',
  data () {
    return {
      user_id: "",
      show_classify: false

    }
  },
  components: {
    user,
    classifier,
    fileupload
  },
  methods: {
    classify: function (event) {
      this.show_classify = !this.show_classify;

    },
    uploadpicture: function (event) {
      axios.post(process.env.API_URL + '/uploadpicture', this.user)
      .then(function(response){
        console.log('saved successfully')
      }
    );}}

  }
  </script>
