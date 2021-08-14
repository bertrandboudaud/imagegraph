<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <hr>
        <h2>Outputs</h2>
          <component v-for="(output, index) in outputs"
                      :key="index"
                      :is="displayParameter(output)"
                      :value="output"
                      :parameter_id="index"
                      :parameter_type="output.user_parameter.type"
                      :ref="index">
          </component>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import OutputCoordinates from '@/components/OutputCoordinates.vue';
import OutputImage from '@/components/OutputImage.vue';
import OutputUnknown from '@/components/OutputUnknown.vue';

export default {
  name: 'Outputs',
  data() {
    return {
      paramComponents: {},
    };
  },
  props:
  {
    outputs: [],
  },
  components: {
    OutputCoordinates,
    OutputImage,
    OutputUnknown,
  },
  methods: {
    displayParameter(param) {
      let paramComponent;
      console.log('---------------');
      console.log(param);
      switch (param.user_parameter.type) {
        case 'Coordinates':
          paramComponent = OutputCoordinates;
          break;
        case 'Image':
          paramComponent = OutputImage;
          break;
        default:
          paramComponent = OutputUnknown;
          break;
      }
      this.paramComponents[param.user_parameter.id] = paramComponent;
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
