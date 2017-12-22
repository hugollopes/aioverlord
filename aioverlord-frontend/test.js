const fs = require('fs');
const axios  = require('axios');

axios.post(`http://localhost:5000/create_classification`).then(() => {
  console.log('classification created successfully');
});
 fs.readFile(`features/step_definitions/steps/neural.jpg`, (err, data)=>{

    let base64Image = new Buffer(data, 'binary').toString('base64');
    //console.log(base64Image);


postdata = {
  file_name: "testpic",
  file_data: base64Image,
}; // set image and strip initial data
// post file base64 encoded.
//axios.post(`${client.globals.devAPIURL}/uploadpicture`, postdata)
axios.post(`http://localhost:5000/uploadpicture`, postdata)
.then(() => {
  console.log('saved successfully');
});
console.log(postdata);
});
