/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_MAPBOX_TOKEN: string;
  readonly VITE_AERIS_CLIENT_ID: string;
  readonly VITE_AERIS_CLIENT_SECRET: string;
  readonly VITE_APP_PUBLIC_PATH: string;
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
