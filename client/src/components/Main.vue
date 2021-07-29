<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test</h1>
        <Inputs/>
      </div>
    </div>
  </div>
</template>

<script>

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
  methods: {
  },
  created() {
  },
};
</script>
