<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test</h1>
        <hr>
        <br>
        <b-form @submit="onSubmit" @reset="onReset">
          <b-form-group v-for="(input, index) in inputs"
                    :key="index"
                    id="form-title-group"
                    :label="input.inputs['parameter name'].value.text"
                    label-for="form-title-input">
                    <component :is="displayParameter(input.inputs['default value'])">
                    </component>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Integer from '@/components/Integer.vue';
import Color from '@/components/Color.vue';

export default {
  data() {
    return {
      inputs: [],
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
      paramComponents: {},
    };
  },
  components: {
    Integer,
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
      let paramComponent; // TODO unknown
      console.log(param);
      switch (param.user_parameter.type) {
        case 'Integer':
          console.log(param.user_parameter);
          paramComponent = Integer;
          break;
        case 'Color':
          console.log(param.user_parameter);
          paramComponent = Color;
          break;
        default:
          paramComponent = 'Integer';
          break;
      }
      this.paramComponents[param.user_parameter.id] = paramComponent;
      paramComponent.test_to_remove = 42;
      return paramComponent;
    },
    executeWorkflow(payload) {
      const path = 'http://localhost:5000/test_create';
      axios.post(path, payload)
        .then(() => {
          // this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          // this.getBooks();
        });
    },
    initForm() {
      this.paramComponents = {};
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {};
      console.log('----------');
      console.log(this.paramComponents);
      Object.keys(this.paramComponents).forEach((key) => {
        const paramComponent = this.paramComponents[key];
        console.log(paramComponent);
        payload[key] = paramComponent.getValue();
      });
      console.log('----------');
      console.log(payload);
      this.executeWorkflow(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
  created() {
    this.getInputs();
  },
};
</script>
