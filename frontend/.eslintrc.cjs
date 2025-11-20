module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true
  },
  extends: ['eslint:recommended', 'plugin:vue/vue3-recommended', 'plugin:prettier/recommended'],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    'vue/multi-word-component-names': 'off', // Optional: erlaubt kurze Namen wie "Home"
    'no-console': 'warn', // Warnung bei console.log
    'no-unused-vars': 'warn' // Warnung bei ungenutzten Variablen
  }
}
