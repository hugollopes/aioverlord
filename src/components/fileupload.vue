<template>

  <div class="row" >
    <div class="col-xs-12">
      <h2>here</h2>
      <div class="file-upload-form">
        Upload an image file:
        <input type="file" @change="previewImage" accept="image/*" ref="inputFile">
      </div>
      <div class="image-preview" v-if="imageData.length > 0">
        <img class="preview" :src="imageData">
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'fileupload',
  data() {
    return {
      imageData: ""  // we will store base64 format of image in this string
    }
  },
  methods: {
    previewImage: function(event) {
      // Reference to the DOM input element
      var input = event.target;
      // Ensure that you have a file before attempting to read it
      if (input.files && input.files[0]) {
        // create a new FileReader to read this image and convert to base64 format
        var reader = new FileReader();
        // Define a callback function to run, when FileReader finishes its job
        var imageData = "";
        reader.onload = (e) => {
          // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
          // Read image as base64 and set to imageData
          this.imageData = e.target.result;
          console.log(this.$refs.inputFile.files[0].file)
          var postdata =  { file_name : this.$refs.inputFile.files[0].name,
            file_data : this.imageData.split(',')[1]};
            axios.post(process.env.API_URL +"/uploadpicture", postdata)
              .then(function(response){
              console.log('saved successfully')
              });
          console.log(postdata);
            //console.log("e.target.result" + e.target.result);
            //console.log("imagedata" + this.imageData);
        }
        // Start the reader job - read file as a data url (base64 format)
        reader.readAsDataURL(input.files[0]);
        //var formData = new FormData();
        //var imagefile = document.querySelector('#file');
        //formData.append("image", imagefile.files[0]);

        //axios.post(process.env.API_URL +"/uploadpicture", this.imageData)
        //  .then(function(response){
        //  console.log('saved successfully')
        //  });
      }
    }
  }



}
</script>
