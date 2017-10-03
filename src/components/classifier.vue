<template>

  <div class="row" >
    <div class="col-xs-12">
      <h2>{{classification.name}}</h2>
      <ul>
        <li v-for="item in classification.images">
          {{ item }}
          <ul>
            <li v-for="option in classification.labels">
              <button v-on:click="classify_choice">{{  option   }}</button>
            </li>
          </ul>
        </li>
      </ul>
      {{classification}}
      {{classifed}}
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
      classifed: false
    }
  },
  created: function(){axios.get("http://127.0.0.1:50000/classify")
  .then(response => {this.classification = response.data});
},
methods: {
  classify_choice: function (event) {
    this.classifed = true;
    axios.post('http://127.0.0.1:50000/saveclassification', {
                "file_id": "59cfa2d58d28793cd091d1a8",
                "labeled": "yes"
            })
      .then(function(response){
        console.log('saved successfully')
      });
  }},
}

</script>
