
<template>
  <div class="topology" id="topologydiv">
    topology
    <button v-on:click="buyNeuron" id="buyNeuronButton">buy Neuron</button>

    </svg>
  </div>
</template>

<script>
import { bus } from '../main';

export default {
  name: 'topology',
  data() {
    return {
      neurons: 0,
    };
  },
  created() {
    bus.$on('neuronsUpdated', (neurons) => {
      this.neurons = neurons;
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
