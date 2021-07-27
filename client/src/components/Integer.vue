<template>
  <div>
    <b-form-input type="number" v-model="param.value" step="0.01" min="0.00" max="1000.00" />
  </div>
</template>

<script>
export default {
  name: 'Integer',
  data() {
    return {
      param: {
        value: 42,
      },
    };
  },
  methods: {
  },
  getValue() {
    console.log('==========');
    console.log(this);
    console.log(this.param.value);
    return this.param.value;
  },
};
</script>
