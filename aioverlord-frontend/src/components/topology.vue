
<template>
  <div class="topology" id="topologydiv">
    topology: {{topologies}}   availableTopologies : {{availableTopologies}}
    <button  :disabled="buyNeuronDisabled" v-on:click="buyNeuron" id="buyNeuronButton">buy Neuron</button>
    <ul>
      <li v-for="topology in availableTopologies">
        <button v-on:click="buyTopology(topology.id)"  v-bind:userId="'buyTopology' + topology.id">buy {{  topology.name   }}</button>
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
