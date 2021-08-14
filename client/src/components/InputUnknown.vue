<template>
  <div>
    <b-alert variant="warning" show>Unknown Input Parameter type: {{parameter_type}}</b-alert>
  </div>
</template>

<script>
export default {
  name: 'InputUnknown',
  props: ['parameter_id', 'default_value', 'parameter_type'],
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
