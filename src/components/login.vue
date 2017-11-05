<template>
  <div class="container">
    <div class="row">
      <div class="col-xs-10 col-xs-offset-1 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
        <div class="panel panel-primary">
          <div class="panel-heading">
            <h3 class="panel-title" id="loginPanel" >Login</h3>
          </div>
          <div class="panel-body">
            <form @submit.prevent="submitLogin">
              <div class="form-group has-feedback" v-bind:class="[emailSuccessClass]">
                <label for="email" class="control-label sr-only">Add your email address.</label>
                <input ref="txtEmail" type="email" class="form-control" @input="checkEmailValidation" id="email" placeholder="Email" autofocus required>
                <span v-bind:class="[emailIconClass]"></span>
              </div>
              <div class="form-group has-feedback" v-bind:class="[passwordSuccessClass]">
                <label for="password" class="control-label sr-only">Add your password.</label>
                <input ref="txtPassword" type="password" class="form-control" @input="checkPasswordValidation" id="password" placeholder="Password" required
                       :pattern="passwordPattern" aria-describedby="passwordHelpSpan">
                <span v-bind:class="[passwordIconClass]"></span>
                <small id="passwordHelpSpan">{{ passwordMessage }}</small>
              </div>
              <div v-if="errorMessage" class="text-center text-danger">{{ errorMessage }}</div>
              <div class="checkbox">
                <label>
                  <input type="checkbox" id="chkRemember" v-model="rememberMe">
                  Remember Me
                </label>
                <button :disabled="submitBtnDisabled" class="btn btn-primary pull-right" id="loginButton">Sign In</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  // original code from here: https://github.com/tcstx/vue-bootstrap3-login-component-tutorial
  export default {
    name: 'LoginComponent',
    props: {
      errorMessage: {
        type: String,
        required: false,
        default: '',
      },
      passwordMessage: {
        type: String,
        required: false,
        default: 'Password length must be greater than 4 but not longer than 10',
      },
      passwordPattern: {
        type: String,
        required: false,
        default: '.{5,10}',
      },
    },
    data() {
      return {
        emailSuccessClass: '',
        passwordSuccessClass: '',
        emailIconClass: '',
        passwordIconClass: '',
        submitBtnDisabled: true,
        rememberMe: false,
      };
    },
    mounted() {
      const email = document.cookie.match('(^|;)\\s*email\\s*=\\s*([^;]+)');
      const password = document.cookie.match('(^|;)\\s*password\\s*=\\s*([^;]+)');
      this.$refs.txtEmail.value = email ? email.pop() : '';
      this.$refs.txtPassword.value = password ? password.pop() : '';
      if (email) this.submitBtnDisabled = false;
      this.$log.debug(`We just check to see if there were cookies: ${document.cookie}`);
    },
    methods: {
      checkEmailValidation() {
        if (this.$refs.txtEmail.checkValidity()) {
          this.emailSuccessClass = 'has-success';
          this.emailIconClass = 'glyphicon glyphicon-ok form-control-feedback';
          if (this.$refs.txtPassword.checkValidity()) this.submitBtnDisabled = false;
        } else {
          this.emailSuccessClass = 'has-error';
          this.emailIconClass = 'glyphicon glyphicon-remove form-control-feedback';
          this.submitBtnDisabled = true;
        }
      },
      checkPasswordValidation() {
        if (this.$refs.txtPassword.checkValidity()) {
          this.passwordSuccessClass = 'has-success';
          this.passwordIconClass = 'glyphicon glyphicon-ok form-control-feedback';
          if (this.$refs.txtEmail.checkValidity()) this.submitBtnDisabled = false;
        } else {
          this.passwordSuccessClass = 'has-error';
          this.passwordIconClass = 'glyphicon glyphicon-remove form-control-feedback';
          this.submitBtnDisabled = true;
        }
      },
      submitLogin() {
        const email = this.$refs.txtEmail.value.trim();
        const password = this.$refs.txtPassword.value.trim();
      // COOKIE FUNCTIONS!
      // 'key=value; expires=current dateTime in UTC; path=/'
        if (this.rememberMe) {
          const d = new Date();
          d.setTime(d.getTime() + (180 * 24 * 60 * 60 * 1000)); //
          document.cookie = `email=${email};expires=${d.toUTCString()};path=/`;
          document.cookie = `password=${password};expires=${d.toUTCString()};path=/`;
          this.$log.debug(`We just set the cookies: ${document.cookie}`);
        } else {
          document.cookie = 'email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
          document.cookie = 'password=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
          this.$log.debug(`We just deleted the cookies: ${document.cookie}`);
        }
        const postdata = {
          username: email,
          password,

        };
        this.$log.debug(postdata);
        axios.post(`${process.env.API_URL}/gettoken`, postdata)
        .then((response) => {
          const token = response.data.token;
          this.$emit('checkCredentials',
            {
              email,
              token,
            },
        );
        });
      },
    },
  };
</script>

<style scoped>
</style>
