<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test</h1>
          <Inputs v-on:workflowEnd="workflowEnd"/>
          <Outputs v-if="hasOutputs()" :outputs="outputs"/>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      outputs: {},
    };
  },
  methods: {
    workflowEnd(payload) {
      this.outputs = payload.data.outputs;
    },
    hasOutputs() {
      return (Object.keys(this.outputs).length > 0);
    },
  },
  created() {
  },
};
</script>
