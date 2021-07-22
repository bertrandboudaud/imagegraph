<template>
  <b-form-input type="number" step="0.01" min="0.00" max="1000.00" />
</template>

<script>
export default {
  name: 'Integer',
  data() {
    return { }
  },
  methods: {
    check() { this.checked = !this.checked; }
  },
};
</script>
