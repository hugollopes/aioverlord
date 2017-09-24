const vm = new Vue({
  el: '#app',
  data: {
    results: []
  },
  mounted() {
    axios.get("http://127.0.0.1:50000/")
    .then(response => {this.results = response.data})
  }
});

