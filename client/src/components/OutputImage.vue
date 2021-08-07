<template>
  <div>
    <h3>
    {{parameter_id}}
    </h3>
    <img :src="value.user_parameter.value">
    <br>
  </div>
</template>

<script>
export default {
  name: 'OutputImage',
  props: ['parameter_id', 'value'],
  data() {
    return {
    };
  },
};
</script>
