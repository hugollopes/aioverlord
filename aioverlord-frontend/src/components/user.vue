<template>
  <div class="row">
    <div class="container">
    <div class="row">
      <div class="col-xs-12 panel" id="userId">{{userId}}</div>
    </div>
    <div class="row">
      <div class="col-xs-1 panel" id="creditsLabel">Credits: </div>
      <div class="col-xs-1 panel panel2" id="credits">{{credits}}</div>
      <div class="col-xs-1 panel" id="neuronsLabel">Neurons:</div>
      <div class="col-xs-1 panel panel2" id="neurons">{{neurons}}</div>
        <div class="col-xs-8" id="filler"></div>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { bus } from '../main';


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
      topologies: [],
      availableTopologies: [],
    };
  },
  mounted() {
    this.run(this.userId);
  },
  created() {
    bus.$on('increaseNeuron', () => {
      const postdata = {
        username: this.userId,
        token: this.token,
      };
      // this.$log.debug(`postdata: ${postdata.token}  ${postdata.username}`);
      axios.post(`${process.env.API_URL}/buy_neuron`, postdata)
      .then((response) => {
        this.$log.debug(response);
        if (response.data === 'not enough credits') {
          this.$log.debug('not enough credits');
        } else {
          this.neurons += 1;
          this.$log.debug('neuron purchased');
        }
      });
    });
    bus.$on('availableTopologies', () => {
      const postdata = {
        username: this.userId,
        token: this.token,
      };
      this.$log.debug(`postdata availableTopologies: ${postdata.token}  ${postdata.username}`);
      axios.post(`${process.env.API_URL}/availableTopologies`, postdata)
      .then((response) => {
        this.$log.debug(response);
        this.availableTopologies = response.data.availableTopologies;
        this.$log.debug('Topologies available');
        bus.$emit('availableTopologiesUpdated', this.availableTopologies);
      });
    });
    bus.$on('buyTopology', (topologyId) => {
      const postdata = {
        username: this.userId,
        token: this.token,
        topologyId,
      };
      this.$log.debug(`postdata buy topology: ${postdata.token}  ${postdata.username}`);
      axios.post(`${process.env.API_URL}/buyTopology`, postdata)
      .then((response) => {
        this.$log.debug(response);
        this.$log.debug(`Topology of id ${topologyId} bought`);
        bus.$emit('availableTopologies');
      });
    });
  },
  methods: {
    run(userId, token) {
      const self = this;
      this.token = token;
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
          this.neurons = response.data.neurons;
          this.topologies = response.data.topologies;
          bus.$emit('neuronsUpdated', this.neurons);
          bus.$emit('creditsUpdated', this.credits);
          bus.$emit('topologiesUpdated', this.topologies);
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
