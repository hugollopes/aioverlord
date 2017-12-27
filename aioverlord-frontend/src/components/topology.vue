
<template>
  <div class="topology" id="topologydiv">
    topology
    <button  :disabled="buyNeuronDisabled" v-on:click="buyNeuron" id="buyNeuronButton">buy Neuron</button>
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
  },
  methods: {
    buyNeuron() {
      bus.$emit('increaseNeuron');
    },


  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
