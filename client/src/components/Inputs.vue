<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h2>Inputs</h2>
        <hr>
        <b-form @submit="onSubmit" @reset="onReset">
          <b-form-group v-for="(input, index) in inputs"
                    :key="index"
                    :id="index"
                    :label="index"
                    label-for="form-title-input">
                    <component :is="displayParameter(input.inputs['default value'])"
                               :default_value="input.inputs['default value']"
                               :parameter_id="index"
                               :ref="index">
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
import InputInteger from '@/components/InputInteger.vue';
import InputColor from '@/components/InputColor.vue';

export default {
  name: 'Inputs',
  data() {
    return {
      inputs: [],
      paramComponents: {},
    };
  },
  components: {
    InputInteger,
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
          paramComponent = InputInteger;
          break;
        case 'Color':
          console.log(param.user_parameter);
          paramComponent = InputColor;
          break;
        default:
          paramComponent = 'InputInteger';
          break;
      }
      this.paramComponents[param.user_parameter.id] = paramComponent;
      return paramComponent;
    },
    executeWorkflow(payload) {
      const path = 'http://localhost:5000/test_create';
      axios.post(path, payload)
        .then((response) => {
          console.log(response);
          this.$emit('workflowEnd', response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    initForm() {
      this.paramComponents = {};
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {};
      Object.keys(this.paramComponents).forEach((key) => {
        const paramComponent = this.$refs[key][0];
        payload[key] = paramComponent.getValue();
      });
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
