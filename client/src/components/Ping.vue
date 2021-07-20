<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test</h1>
        <hr>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Input name</th>
              <th scope="col">Value</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(input, index) in inputs" :key="index">
              <td>{{ input.inputs["parameter name"].value.text }}</td>
              <!--<td>{{ input.inputs["default value"].user_parameter.value.value }}</td>-->
              <td>{{ displayParameter(input.inputs["default value"]) }}</td>
            </tr>
          </tbody>
        </table>
        <br>
        <button type="button" class="btn btn-success btn-sm">Lanch workflow</button>
        <br>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputs: [],
    };
  },
  methods: {
    getInputs() {
      const path = 'http://localhost:5000/test_create';
      axios.get(path)
        .then((res) => {
          // console.log(res.data);
          this.inputs = res.data.inputs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    displayParameter(param) {
      console.log(param);
      switch (param.user_parameter.type) {
        case 'Integer':
          return 'integer';
        default:
          return 'prout';
      }
    },
  },
  created() {
    this.getInputs();
  },
};
</script>
