<template>
  <div id="main" class="container">
    <div class="row header">
      <div class="col">
        <h1 class="text-center" id="title">AI Overlord</h1></div>
    </div>
    <login v-on:checkCredentials="checkCredentials($event)" v-show="showLogin">
      :errorMessage="errorMessage"
      passwordPattern=".{2,8}"
      passwordMessage="Greater than 1 and less than 9"
    </login>
    <user ref="user"  v-bind:userId="userId"  v-show="!showLogin"></user>
    <classifier v-show="show_classify"
    v-bind:classification="classification"
    v-on:changeShowClassify="changeShowClassify()"></classifier>
    <component v-bind:is="NeuralNetArea" v-show="!showLogin"></component>
    <div class="row">
      <div class="col-xs-12" v-show="!showLogin" id="buttonsDiv">
        <button v-on:click="ShowTopology" id="topologyButton" v-show="showTopologyButton">topology</button>
        <button v-on:click="showNetwork" id="showNetworkButton" v-show="showNetworkButton">Network</button>
        <button v-on:click="ShowWorld" id="ShowWorldButton" v-show="ShowWorldButton">world</button>
        <button v-on:click="classify">trainNN/nnconfig</button>
        <button v-on:click="classify">data sets</button>
        <button id="Downmenubutton" v-on:click="classify">label data</button>
      </div>
    </div>
    <div class="row">

      <div class="col-xs-12" v-show="!showLogin">
        <h1>debug functions!!!</h1>
        <button id="debugFunctions"  v-on:click="fileupload">file upload</button>
      </div>
    </div>
  </div>
</template>
<script>
import user from '@/components/user';
import classifier from '@/components/classifier';
import fileupload from '@/components/fileupload';
import neuralnet from '@/components/neuralnet';
import topology from '@/components/topology';
import login from '@/components/login';
import world from '@/components/world';
import axios from 'axios';


export default {
  name: 'main',
  data() {
    return {
      userId: '',
      token: '',
      showLogin: true,
      classification: {},
      show_classify: false,
      showTopologyButton: true,
      showNetworkButton: false,
      ShowWorldButton: true,
      NeuralNetArea: 'neuralnet', // indicates  what component is visible in that area
    };
  },
  components: {
    user,
    classifier,
    fileupload,
    neuralnet,
    login,
    topology,
    world,
  },
  methods: {
    changeShowClassify() {
      this.$log.debug('classification.show_classify');
      this.show_classify = false;
    },
    ShowTopology() {
      this.NeuralNetArea = 'topology';
      this.showTopologyButton = false;
      this.showNetworkButton = true;
    },
    ShowWorld() {
      this.NeuralNetArea = 'world';
      this.showTopologyButton = false;
      this.showNetworkButton = true;
      this.showWorldButton = false;
    },
    showNetwork() {
      this.NeuralNetArea = 'neuralnet';
      this.showTopologyButton = true;
      this.showNetworkButton = false;
    },
    classify() {
      const postdata = {
        username: this.userId,
        token: this.token,
      };
      this.$log.debug(`postdata: ${postdata.token}  ${postdata.username}`);
      axios.post(`${process.env.API_URL}/classify`, postdata)
      .then((response) => {
        this.$log.debug(response);
        if (response.data === 'no results') {
          this.$log.debug('nothing to classify');
        } else {
          this.classification = response.data;
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
    runTicker(userId, token) {
      this.$refs.user.run(userId, token);
    },
    checkCredentials(event) {
      this.userId = event.email;
      this.token = event.token;
      this.$log.debug(`Email is: ${event.email}`);
      this.$log.debug(`token is: ${event.token}`);
      this.showLogin = false;
      this.runTicker(this.userId, event.token);
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
