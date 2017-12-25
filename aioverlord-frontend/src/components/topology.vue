
<template>
  <div class="topology" id="topologydiv">
    topology

    </svg>
  </div>
</template>

<script>
export default {
  name: 'topology',
  data() {
    return {
      neurons: 100,
    };
  },
  methods: {
    buy_neuron() {
      console.log("buy neurons");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
