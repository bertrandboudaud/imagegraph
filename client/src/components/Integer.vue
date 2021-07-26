<template>
  <b-form-input type="number" v-model="param.value" step="0.01" min="0.00" max="1000.00" />
</template>

<script>
export default {
  name: 'Integer',
  data() {
    return {
      param: {
        value: 0,
      },
    };
  },
  methods: {
    getValue() { return this.param; },
  },
};
</script>
