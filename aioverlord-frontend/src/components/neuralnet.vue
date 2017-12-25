
<template>
  <div class="network">
    <svg id = "networksvg" height="500" width="500">
    <circle v-for="neuron in neurons"

          v-bind:cx="neuron.coordinate_x"
          v-bind:cy="neuron.coordinate_y" v-bind:id="neuron.id" r="4" stroke="black" stroke-width="3" fill="blue" />

    <g v-for="synapse in synapses" fill="none" stroke="grey" stroke-width="1">
      <path stroke-dasharray="5,5" v-bind:d="synapse.d" v-bind:id="synapse.id" />
    </g>

    </svg>
  </div>
</template>

<script>
export default {
  name: 'neuralnet',
  mounted() {
    this.generate_network(2, 5);
  },
  data() {
    return {
      svgHeight: 1000,  // not being used. fix!
      canvasWidth: 450, // not being used. fix!
      neurons: [],
      synapses: [],
      neuron_distance: 100, // distance between neurons.
    };
  },
  methods: {
    generate_network(numLayers, numNeurons) {
      const neurons = [];
      for (let i = 0; i < numLayers; i += 1) {
        for (let j = 0; j < numNeurons; j += 1) {
          const neuronId = `neuron${String(i)}_${String(j)}`;
            // console.log(neuron_id);
          const neuron = {
            id: neuronId,
            layer: i,
            neuron: j,
            coordinate_x: 100 + (i * this.neuron_distance),
            coordinate_y: 100 + (j * this.neuron_distance),
          };
          neurons.push(neuron);
        }
      }
      const synapses = [];

      for (let i = 0; i < neurons.length; i += 1) {
        for (let j = 0; j < neurons.length; j += 1) {
          if ((neurons[i].id !== neurons[j].id) && (neurons[i].layer !== neurons[j].layer)) {
            const synapseId = `syn${neurons[i].id}${neurons[j].id}`;
            const synapse = {
              x1: neurons[i].coordinate_x,
              y1: neurons[i].coordinate_y,
              x2: neurons[j].coordinate_x,
              y2: neurons[j].coordinate_y,
              d: `M${String(neurons[i].coordinate_x)} ${
              String(neurons[i].coordinate_y)
              } l${String(neurons[j].coordinate_x - neurons[i].coordinate_x)} ${
              String(neurons[j].coordinate_y - neurons[i].coordinate_y)}`,
              id: synapseId,
            };
            synapses.push(synapse);
          }
        }
      }
      this.neurons = neurons;
      this.synapses = synapses;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
