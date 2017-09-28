const vm = new Vue({
  el: '#app',
  data: {
    results: []
  },
  mounted() {
    axios.get("http://10.0.2.2:50000/")
    .then(response => {this.results = response.data})
  }
});

