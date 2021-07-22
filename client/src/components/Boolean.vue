<template>
    <div class="checkbox-wrapper" @click="check">
      <div :class="{ checkbox: true, checked: checked }"></div>
      <div class="title">{{ title }}</div>
    </div>
</template>

<script>
export default {
  name: 'Integer',
  data() {
    return { checked: false, title: 'Check me' }
  },
  methods: {
    check() { this.checked = !this.checked; }
  },
};
</script>
