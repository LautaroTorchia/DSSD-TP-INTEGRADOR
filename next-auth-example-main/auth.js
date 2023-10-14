import { getServerSession } from "next-auth"
import CredentialProvider from "next-auth/providers/credentials";
import axios from "axios";

// Read more at: https://next-auth.js.org/getting-started/typescript#module-augmentation


export const config = {
  providers: [
    CredentialProvider({
      name: "credentials",
      credentials: {
        username: {
          label: "Email",
          type: "text",
          placeholder: "",
        },
        password: { label: "Contraseña", type: "password" },
      },
      authorize: async (credentials) => {
        const response = await axios.post("http://localhost:8000/api/auth/login/", {
          email: credentials.username,
          password: credentials.password,
        })
        if (response) { return response.data }
        return null
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.email;
        token.accessToken = user.tokens.access;
        token.userRole = "admin"
      }
      return token
    },
    session: ({ session, token }) => {
      if (token) {
        session.id = token.id;
        session.accessToken = token.accessToken;
      }
      return session;
    },
  },
  secret: "c620d99c0fd7142c3fb4b55ac9b23103",
  jwt: {
    secret: "c620d99c0fd7142c3fb4b55ac9b23103",
    encryption: true,
  },
}

export function auth(...args) {
  return getServerSession(...args, config)
}

