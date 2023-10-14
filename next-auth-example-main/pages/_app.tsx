import { SessionProvider } from "next-auth/react"
import "./styles.css"
import type { AppProps } from "next/app"
import type { Session } from "next-auth"
import dynamic from "next/dynamic"
import React from "react"


// Use of the <SessionProvider> is mandatory to allow components that call
// `useSession()` anywhere in your application to access the `session` object.

const App = ({
  Component,
  pageProps: { session, ...pageProps },
}: AppProps<{ session: Session }>) => {
  return (
    <SessionProvider session={session}>
      <Component {...pageProps} />
    </SessionProvider>
  )
};

export default dynamic(() => Promise.resolve(App), {
  ssr: false,
});