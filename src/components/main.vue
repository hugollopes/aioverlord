<template>
  <div id="main">
    <div class="row">
      <div><h2 class="text-center">AI Overlord</h2></div>
    </div>
    <user></user>
    {{show_classify}}
    <classifier v-show="show_classify"
        v-bind:classification="classification"
        v-on:changeShowClassify="changeShowClassify()"></classifier>
    <div class="row">
      <div class="col-12">
        <img src="../images/neural.jpg" class="rounded mx-auto d-block"
        alt="Responsive image" height="100">
      </div>
    </div>
    <component v-bind:is="NeuralNetArea"></component>

    <div class="row">
      <div class="col-xs-12">
        <button v-on:click="classify">topology</button>
        <button v-on:click="classify">trainNN/nnconfig</button>
        <button v-on:click="classify">data sets</button>
        <button v-on:click="classify">label data</button>
      </div>
    </div>
    <div class="row">

      <div class="col-xs-12">
          <h1>debug functions!!!</h1>
        <button v-on:click="fileupload">file upload</button>
      </div>
    </div>
  </div>
</template>
<script>
import user from '@/components/user';
import classifier from '@/components/classifier';
import fileupload from '@/components/fileupload';
import neuralnet from '@/components/neuralnet';
import axios from 'axios'


export default {
  name: 'main',
  data () {
    return {
      user_id: "",
      classification: {},
      show_classify : false,
      NeuralNetArea : "neuralnet"

    }
  },
  components: {
    user,
    classifier,
    fileupload,
    neuralnet
  },
  methods: {
    changeShowClassify: function (){
      console.log("classification.show_classify")
      this.show_classify = false;
    },
    classify: function (event) {
      axios.get(process.env.API_URL +"/classify")
      .then(response => {this.classification = response.data; //todo: fix the string concat bellow
                          this.classification.image = "data:image/jpg;base64," + this.classification.image;
                          this.show_classify = true;
                          });
    },
    fileupload: function () {
      if( this.NeuralNetArea == "neuralnet" ){
        this.NeuralNetArea = "fileupload";
      }
      else {
        this.NeuralNetArea = "neuralnet";
      }
    }
  }

  }
  </script>
