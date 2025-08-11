/// <reference types="vite/client" />

// Optional: declare your custom env vars for better type support
interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
}
interface ImportMeta {
  readonly env: ImportMetaEnv
}


