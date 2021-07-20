<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Test</h1>
        <hr>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Input name</th>
              <th scope="col">Value</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(input, index) in inputs" :key="index">
              <td>{{ input.inputs["parameter name"].value.text }}</td>
              <!--<td>{{ input.inputs["default value"].user_parameter.value.value }}</td>-->
              <td>{{ displayParameter(input.inputs["default value"]) }}</td>
            </tr>
          </tbody>
        </table>
        <br>
        <button type="button" class="btn btn-success btn-sm">Lanch workflow</button>
        <br>
        <b-form @submit="onSubmit" @reset="onReset">
          <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
            <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
              <b-form-checkbox value="true">Read?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputs: [],
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
    };
  },
  methods: {
    getInputs() {
      const path = 'http://localhost:5000/test_create';
      axios.get(path)
        .then((res) => {
          // console.log(res.data);
          this.inputs = res.data.inputs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    displayParameter(param) {
      console.log(param);
      switch (param.user_parameter.type) {
        case 'Integer':
          return 'integer';
        default:
          return 'prout';
      }
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.read = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      let read = false;
      if (this.addBookForm.read[0]) read = true;
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getInputs();
  },
};
</script>
