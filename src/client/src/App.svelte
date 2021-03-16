<script lang="ts">
  import ProblemForm from './ProblemForm.svelte'
  import QueryForm from './QueryForm.svelte'
</script>

<main>
  <div class="container">
    <div class="problem-form">
      <ProblemForm />
    </div>
    <div class="query-form">
      <QueryForm />
    </div>
  </div>
  <footer>
    <a href="https://github.com/AleksTeresh/master-thesis" target="_blank"
      >GitHub repo</a
    >
    <a href="https://research.cs.aalto.fi/da/" target="_blank"
      >Our research group</a
    >
    <p class="narrow-paragraph">
      The authors wish to acknowledge <a href="https://www.csc.fi/en" target="_blank">CSC – IT Center for Science, Finland</a>, for computational resources.
    </p>
  </footer>
</main>

<style>
  .container {
    min-height: calc(100vh - 70px);
    display: flex;
    justify-content: space-between;
  }

  .problem-form {
    flex-basis: 35%;
  }

  .query-form {
    flex-basis: 65%;
  }

  .narrow-paragraph {
    display: inline-block;
  }

  main {
    height: 100%;
  }

  footer {
    background-color: rgba(218, 216, 216, 0.473);
    min-height: 70px;
    font-size: 15px;

    display: flex;
    justify-content: center;
    align-items: center;
  }

  footer > * {
    margin-left: 20px;
    margin-right: 20px;
  }
</style>
