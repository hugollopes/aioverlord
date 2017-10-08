<template>

  <div class="row" >
    <div class="col-xs-12">
      <h1>{{classification.name}}</h1>
        <h2>{{classification.image_name}}</h2>
        <img v-bind:src="classification.image" height="50"/>
          <ul>
            <li v-for="option in classification.labels">
              <button v-on:click="classify_choice(option)" ref="option">{{  option   }}</button>
            </li>
          </ul>

      {{classification}}
    </div>
  </div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'classifier',
  data () {
    return {
      classification: {},
      classifed : false
    }
  },
  created: function(){axios.get(process.env.API_URL +"/classify")
  .then(response => {this.classification = response.data //todo: fix the string concat bellow
                      this.classification.image = "data:image/jpg;base64," + this.classification.image
                      });
},
methods: {
  classify_choice: function (choice) {
    this.classifed = true;
    var postdata =  { "file_id": this.classification.file_id,
      labeled : choice};
    console.log(postdata);
    axios.post(process.env.API_URL + '/saveclassification', postdata)
      .then(function(response){
        console.log('saved successfully')
      });
  }},
}

</script>
