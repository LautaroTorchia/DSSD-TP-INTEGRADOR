import AuthorizationMiddleware from "@/components/authorizationMiddleware";


export default function PrivateLayout({ children }) {
  return (
    <div>
      {/* Add private layout components like header, footer, etc. */}
      <AuthorizationMiddleware>{children}</AuthorizationMiddleware>
    </div>
  );
}