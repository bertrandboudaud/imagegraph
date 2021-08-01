<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h2>Outputs</h2>
        <hr>
          <component v-for="(output, index) in outputs"
                      :key="index"
                      :is="displayParameter(output.inputs['default value'])"
                      :default_value="input.inputs['default value']"
                      :parameter_id="index"
                      :ref="index">
          </component>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InputInteger from '@/components/InputInteger.vue';
import InputColor from '@/components/InputColor.vue';

export default {
  data() {
    return {
      outputs: [],
      paramComponents: {},
    };
  },
  components: {
    InputInteger,
  },
  methods: {
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
        const paramComponent = this.$refs[key][0];
        payload[key] = paramComponent.getValue();
      });
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
  },
};
</script>
