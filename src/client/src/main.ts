import 'normalize.css/normalize.css'
import 'milligram/dist/milligram.min.css'
import './global.css'

import App from './App.svelte'

// see global.d.ts
Object.typedKeys = Object.keys as any

const app = new App({
  target: document.body,
})

export default app
