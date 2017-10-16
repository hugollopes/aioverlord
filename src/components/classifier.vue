<template>

  <div class="row" >
    <div class="col-xs-12">
      {{classification.show_classify}}
      <h1 id="classificationName">{{classification.name}}</h1>
      <h2>{{classification.image_name}}</h2>
      <img v-bind:src="classification.image" height="50"/>
      <ul>
        <li v-for="option in classification.labels">
          <button v-on:click="classify_choice(option)" ref="option">{{  option   }}</button>
        </li>
      </ul>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'classifier',
  props: ['classification'],
  data() {
    return {
      classifed: false,
    };
  },
  methods: {
    classify_choice(choice) {
      const postdata = { file_id: this.classification.file_id,
        labeled: choice,
      };
      this.classifed = true;

      // todo: find console logging object.
      console.log(postdata);
      this.$emit('changeShowClassify');
      axios.post(`${process.env.API_URL}/saveclassification`, postdata)
      .then(() => {
        console.log('saved successfully');
      });
    },
  },
};
</script>
