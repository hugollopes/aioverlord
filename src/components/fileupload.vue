<template>

  <div class="row">
    <div class="col-xs-12">
      <div class="file-upload-form">
        Upload an image file(jpg):
        <input Id="fileuploadarea" type="file" @change="previewImage" accept="image/*" ref="inputFile">
      </div>
      <div class="image-preview" v-if="imageData.length > 0">
        <img class="preview" :src="imageData">
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: 'fileupload',
  data() {
    return {
      imageData: '',  // we will store base64 format of image in this string
    };
  },
  methods: {
    previewImage(event) {
      // Reference to the DOM input element
      const input = event.target;
      let postdata = {};
      // create a new FileReader to read this image and convert to base64 format
      const reader = new FileReader();
      // Ensure that you have a file before attempting to read it
      if (input.files && input.files[0]) {
        reader.onload = (e) => {
          // Read image as base64 and set to imageData
          this.imageData = e.target.result;
          // console.log(this.$refs.inputFile.files[0].file)
          postdata = {
            file_name: this.$refs.inputFile.files[0].name,
            file_data: this.imageData.split(',')[1],
          }; // set image and strip initial data
          // post file base64 encoded.
          axios.post(`${process.env.API_URL}/uploadpicture`, postdata)
          .then(() => {
            this.$log.debug('saved successfully');
          });
          this.$log.debug(postdata);
        };
        // Start the reader job - read file as a data url (base64 format)
        reader.readAsDataURL(input.files[0]);
      }
    },
  },
};
</script>
