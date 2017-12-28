
<template>
  <div class="network">
    <svg id = "networksvg" v-bind:height="this.svgHeight" v-bind:width="this.svgWidth">
    <circle v-for="neuron in neurons"
          v-bind:cx="neuron.coordinate_x"
          v-bind:cy="neuron.coordinate_y" v-bind:id="neuron.id"
          v-bind:r="neuron_circle_size" stroke="black" stroke-width="3" fill="blue" />
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
      svgHeight: 550,
      svgWidth: 450,
      neurons: [],
      synapses: [],
      neuron_distance: 100, // distance between neurons.
      neuron_circle_size: 6,
      svg_padding: 10,

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
            coordinate_x: this.svg_padding + this.neuron_circle_size
              + this.neuron_distance + (i * this.neuron_distance),
            coordinate_y: this.svg_padding + this.neuron_circle_size
              + (j * this.neuron_distance),
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
      // todo: input neurons: this.inputNeurons = [{x1:0,y1:0},{x2:0,y2:this.neuron_distance}]
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.network  {
    padding: 2rem 1rem;
}
</style>
