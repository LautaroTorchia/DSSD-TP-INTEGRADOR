import Navbar from '../components/Navbar';
import styles from '../styles/Home.module.css'; // Import your custom styles

export default function Home() {
  return (
    <div className={styles.container}>
      <Navbar />
      <header className={styles.header}>
        <h1 className={styles.title}>Bienvenido a Global Furniture</h1>
        <p className={styles.subtitle}>Descubre nuestras colecciones de muebles sostenibles.</p>
      </header>

      <footer className={styles.footer}>
        {/* Add footer content here */}
      </footer>
    </div>
  );
}
