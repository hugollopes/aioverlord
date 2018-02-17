
<template>
  <div class="topology" id="topologydiv">
    <button  :disabled="buyNeuronDisabled" v-on:click="buyNeuron" id="buyNeuronButton">buy Neuron</button>
    <div class="container">
    <div class="row" >
      <div class="col-xs-2 panel2">  topologies bought:</div>
    </div>
    <div class="row" v-for="topology in topologies">
      <div class="col-xs-2 panel" v-bind:Id="'topologyOwned' + topology.id">{{topology.name}}</div>
    </div>
    </div>
    <ul>
      <li v-for="topology in availableTopologies">
        <button :disabled="topology.enabledComputed == 'false'" v-on:click="buyTopology(topology.id)"  v-bind:Id="'buyTopology' + topology.id">buy {{  topology.name   }} for {{  topology.cost   }}</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { bus } from '../main';

export default {
  name: 'topology',
  data() {
    return {
      neurons: 0,
      credits: 0,
      topologies: [],
      availableTopologies: [],
    };
  },
  computed: {
    buyNeuronDisabled() {
      if (this.credits < 100) { return true; }
      return false;
    },
  },
  created() {
    bus.$on('neuronsUpdated', (neurons) => {
      this.neurons = neurons;
    });
    bus.$on('creditsUpdated', (credits) => {
      this.credits = credits;
    });
    bus.$on('topologiesUpdated', (topologies) => {
      this.topologies = topologies;
    });
    bus.$on('availableTopologiesUpdated', (availableTopologies) => {
      this.availableTopologies = availableTopologies;
    });
    bus.$emit('availableTopologies');
  },
  methods: {
    buyNeuron() {
      bus.$emit('increaseNeuron');
    },
    buyTopology(topologyId) {
      bus.$emit('buyTopology', topologyId);
    },

  },
};
</script>



<style scoped>
.panel  {

  background-color: lightblue;
      margin-bottom: 0px;
}
.panel2  {
  background-color: pink;
      margin-bottom: 0px;
}



</style>
