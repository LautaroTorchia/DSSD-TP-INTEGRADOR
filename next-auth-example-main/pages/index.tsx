import Layout from "../components/layout"
import styles from '../styles/Home.module.css'; 

export default function IndexPage() {
  return (
    <Layout>
      <h1 className={styles.title}>Bienvenido a Global Furniture</h1>
      <p className={styles.subtitle}>Descubre nuestras colecciones de muebles sostenibles.</p>
    </Layout>
  )
}
