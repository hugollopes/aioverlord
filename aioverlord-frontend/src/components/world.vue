
<template>

  <div class="world" id="worlddiv">

    <div class="row" v-for="agent in agents">
      <div class="col-xs-3 panel" v-bind:Id="'availableagent' + agent.id">
        {{agent.name}}
        <button  v-on:click="buyAgent(agent.id)"  v-bind:Id="'buyAgent' + agent.id">buy {{  agent.name   }} for 10</button>
      s</div>
    </div>
  </div>
</template>

<script>
import { bus } from '../main';
import referenceData from '../assets/referenceData.json';

export default {
  name: 'world',
  data() {
    return {
      neurons: 0,
      credits: 0,
      agents: [{name: "weak agent",id: "4545"},{name: "medium agent",id: "453345"},{name: "strong agent",id: "453345444"}],
      availableTopologies: [],
    };
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
    buyAgent() {
  this.$log.debug(`buying agent...`);
        bus.$emit('buyAgent', topologyId);
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
