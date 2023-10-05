import dynamic from "next/dynamic";
import React from "react";

import 'bootstrap/dist/css/bootstrap.css'
// own css files here
export function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default dynamic(() => Promise.resolve(App), {
  ssr: false,
});
// add bootstrap css 
