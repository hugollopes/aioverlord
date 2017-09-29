const vm = new Vue({
  el: '#app',
  data: {
  isShow: false,
    user: []
  },
  mounted() {
    axios.get("http://127.0.0.1:50000/getuser")
    .then(response => {this.user = response.data})
  },
   methods: {
    tick: function (event) {
      // `this` inside methods point to the Vue instance
      // `event` is the native DOM event
      this.user.cash = this.user.cash + 1 + this.user.factory1Level*1 + this.user.factory2Level*10;

    },
      raiselevel1: function (event) {
      // `this` inside methods point to the Vue instance
      // `event` is the native DOM event
      if(this.user.cash >= 10){
        this.user.factory1Level = this.user.factory1Level +1;
        this.user.cash = this.user.cash - 10;}
      },
      raiselevel2: function (event) {
      // `this` inside methods point to the Vue instance
      // `event` is the native DOM event
      if(this.user.cash >= 100){
        this.user.factory2Level = this.user.factory2Level + 1;
        this.user.cash = this.user.cash - 100;}
      },
        saveuser: function (event) {
      // `this` inside methods point to the Vue instance
      // `event` is the native DOM event
      axios.post('http://127.0.0.1:50000/saveuser', this.user)
  .then(function(response){
    console.log('saved successfully')
  });},


      run: function(){
    const self = this;
    this.intervalid1 = setInterval(function(){
        self.user.cash = self.user.cash + 1 + self.user.factory1Level*1 + self.user.factory2Level*10;
        console.log (this.changes);
    }, 1000);
    }


    }

});

