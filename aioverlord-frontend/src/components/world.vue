
<template>

  <div class="world" id="worlddiv">

    <div class="row" v-for="agent in availableAgents">
      <div class="col-xs-3 panel" v-bind:Id="'availableAgent' + agent.id">
        {{agent.name}}
        <button  v-on:click="buyAgent(agent.id)"  v-bind:Id="'buyAgent' + agent.id">buy {{  agent.name   }} for {{  agent.cost   }} </button>
      </div>
    </div>
    <div class="row" v-for="agent in agents">
      <div class="col-xs-3 panel" v-bind:Id="'agentsOwned' + agent.id">{{agent.name}} with status {{agent.status}}<ul>
          <li v-for="task in tasks">
            <button  v-on:click="assignAgent(agent.id,task.id)"  v-bind:Id="'assignAgent' + agent.id + 't' + task.id">assign {{  agent.name   }} to {{  task.name   }}</button>
          </li>
        </ul>
      </div>
    </div>
    <div class="row" v-for="task in tasks">
      <div class="col-xs-3 panel" >{{task.name}} and it is {{task.status}} </div>
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
      agents: [],
      availableAgents: [],
      agents: [],
      tasks: [],
    };
  },
  created() {
    bus.$on('neuronsUpdated', (neurons) => {
      this.neurons = neurons;
    });

    bus.$on('creditsUpdated', (credits) => {
      this.credits = credits;
    });
    bus.$on('agentsUpdated', (agents) => {
      this.agents = agents;
    });
    bus.$on('tasksUpdated', (tasks) => {
      this.tasks = tasks;
    });
    bus.$on('availableAgentsUpdated', (availableAgents) => {
      this.availableAgents = availableAgents;
    });
    bus.$emit('availableAgents');
  },
  methods: {
    buyAgent(agentId) {
        this.$log.debug(`buying agent...`);
        bus.$emit('buyAgent', agentId);
        bus.$emit('availableAgents');
    },
    assignAgent(agentId,taskId) {
        this.$log.debug(`assign agent...`);
        bus.$emit('assignAgent', agentId,taskId);
        //bus.$emit('availableAgents');
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
