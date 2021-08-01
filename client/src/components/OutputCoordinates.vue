<template>
  <div>
    <h3>
    {{parameter_id}}
    </h3>
    x:{{value.user_parameter.value.x}}
    <br>
    y:{{value.user_parameter.value.y}}
  </div>
</template>

<script>
export default {
  name: 'OutputCoordinates',
  props: ['parameter_id', 'value'],
  data() {
    return {
    };
  },
};
</script>
