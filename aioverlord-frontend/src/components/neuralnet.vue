
<template>
  <div class="hello">
    <canvas id="networkcanvas" ref="canvas" width="500" height="500"></canvas>
  </div>
</template>

<script>
export default {
  name: 'neuralnet',
  mounted() {
    this.canvas = this.$refs.canvas;
    this.context = this.canvas.getContext('2d');
    this.generate_network(2,5);
  },
  data() {
    return {
      canvas: {},
      context: {},
      canvasHeight: 1000,  // not being used. fix!
      canvasWidth: 450,// not being used. fix!
      neurons: [],
      synapses: [],
      neuron_distance: 100, // distance between neurons.
    };
  },
  methods: {
    generate_network(num_layers,num_neurons) {
      let neurons = new Array();
      for (var i = 0; i < num_layers; i++) {
          for (var j = 0; j < num_neurons; j++) {
            let neuron_id= String(i)+"_"+String(j);
            //console.log(neuron_id);
            var neuron = {
              id: neuron_id,
               layer:i,
               neuron:j,
               coordinate_x: 100+ i*this.neuron_distance,
               coordinate_y: 100+ j*this.neuron_distance,
             }
             neurons.push(neuron);
             this.context.beginPath();
             this.context.arc(neuron.coordinate_x, neuron.coordinate_y, 10, 0, 2 * Math.PI);
             this.context.stroke();
          }
      }
      let synapses = new Array();

      for(var i= 0; i < neurons.length ; i++){

        for(var j= 0; j < neurons.length ; j++) {

          if((neurons[i].id !== neurons[j].id )&& (neurons[i].layer !== neurons[j].layer)){
            var synapse_id = neurons[i].id + neurons[j].id;
            synapses[synapse_id] = {
              x1 : neurons[i].coordinate_x,
              y1 : neurons[i].coordinate_y,
              x2 : neurons[j].coordinate_x,
              y2 : neurons[j].coordinate_y,
            }
            this.context.beginPath();
            this.context.moveTo(synapses[synapse_id].x1, synapses[synapse_id].y1);
            this.context.lineTo(synapses[synapse_id].x2, synapses[synapse_id].y2);
            this.context.lineWidth = 1;
            this.context.strokeStyle = '#00aaa';
            this.context.lineCap = 'butt';
            this.context.stroke();
        }}
      }
      this.neurons= neurons;
      this.synapses= synapses;
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
