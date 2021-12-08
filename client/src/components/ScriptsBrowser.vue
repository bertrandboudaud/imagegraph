<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <hr>
        <h2>Graphs</h2>
        <b-dropdown id="graphs" text="Graphs" class="m-md-2">
          <b-dropdown-item v-for="(graph, index) in graphs" :key="index">
            {{graph}}
          </b-dropdown-item>
        </b-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ScriptsBrowser',
  data() {
    return {
      graphs: [],
      url: 'http://localhost:5000/list',
    };
  },
  components: {
  },
  methods: {
    getGraphs() {
      axios.get(this.url)
        .then((res) => {
          console.log(res);
          this.graphs = res.data.graphs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getGraphs();
  },
};
</script>
