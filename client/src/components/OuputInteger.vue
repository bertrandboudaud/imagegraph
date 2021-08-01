<template>
  <div>
    <b-form-input type="number"
                  v-model="param.value"
                  step="0.01"
                  min="0.00"
                  max="1000.00"
                  />
  </div>
</template>

<script>
export default {
  name: 'InputInteger',
  props: ['parameter_id', 'default_value'],
  data() {
    return {
      param: {
        value: this.default_value.user_parameter.value.value,
      },
    };
  },
  methods: {
    getValue() {
      return this.param.value;
    },
  },
};
</script>
