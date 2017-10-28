<template>
  <div id="main" class="container">
    <div class="row header">
      <div class="col">
        <h1 class="text-center" id="title">AI Overlord</h1></div>
    </div>
    <login v-on:checkCredentials="checkCredentials($event)">
      :errorMessage="errorMessage"
      passwordPattern=".{2,8}"
      passwordMessage="Greater than 1 and less than 9"
    </login>
    <user ref="user"  v-bind:userId="userId"></user>
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
        <button id="Downmenubutton" v-on:click="classify">label data</button>
      </div>
    </div>
    <div class="row">

      <div class="col-xs-12">
        <h1>debug functions!!!</h1>
        <button id="debugFunctions"  v-on:click="fileupload">file upload</button>
        <button id="runTicker"  v-on:click="runTicker">run Ticker</button>
      </div>
    </div>
  </div>
</template>
<script>
import user from '@/components/user';
import classifier from '@/components/classifier';
import fileupload from '@/components/fileupload';
import neuralnet from '@/components/neuralnet';
import login from '@/components/login';
import axios from 'axios';


export default {
  name: 'main',
  data() {
    return {
      userId: '',
      classification: {},
      show_classify: false,
      NeuralNetArea: 'neuralnet',
    };
  },
  components: {
    user,
    classifier,
    fileupload,
    neuralnet,
    login,
  },
  methods: {
    changeShowClassify() {
      this.$log.debug('classification.show_classify');
      this.show_classify = false;
    },
    classify() {
      axios.get(`${process.env.API_URL}/classify`)
      .then((response) => {
        this.$log.debug(response);
        if (response.data === 'no results') {
          this.$log.debug('nothing to classify');
        } else {
          this.classification = response.data; // todo: fix the string concat bellow
          this.classification.image = `data:image/jpg;base64,${this.classification.image}`;
          this.show_classify = true;
        }
      });
    },
    fileupload() {
      if (this.NeuralNetArea === 'neuralnet') {
        this.NeuralNetArea = 'fileupload';
      } else {
        this.NeuralNetArea = 'neuralnet';
      }
    },
    runTicker() {
      this.$refs.user.run();
    },
    checkCredentials(event) {
      this.userId = event.email;
      this.$log.debug(`Email is: ${event.email}`);
      this.$log.debug(`Password is: ${event.password}`);
    },
  },
};
</script>

<style scoped>
.header  {
    color: grey;
    padding: 2rem 1rem;
    background-color: #e9ecef;
    border-radius: .3rem;
}
</style>
