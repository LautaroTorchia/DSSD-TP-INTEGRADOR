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
      <main className={styles.mainContent}>
        <section className={styles.featuredCollections}>
          <h2>Destacadas</h2>
          <div className={styles.collectionItem}>
            <img src="/image1.jpg" alt="Collection 1" className={styles.collectionImage} />
            <h3>Nombre de la Colección 1</h3>
            <p>Descripción de la Colección 1.</p>
            <button className={styles.viewButton}>Ver Detalles</button>
          </div>
          <div className={styles.collectionItem}>
            <img src="/image2.jpg" alt="Collection 2" className={styles.collectionImage} />
            <h3>Nombre de la Colección 2</h3>
            <p>Descripción de la Colección 2.</p>
            <button className={styles.viewButton}>Ver Detalles</button>
          </div>
          {/* Add more featured collections here */}
        </section>
        <section className={styles.latestNews}>
          <h2>Últimas Noticias</h2>
          <div className={styles.newsItem}>
            <h3>Título de la Noticia 1</h3>
            <p>Descripción de la Noticia 1.</p>
            <button className={styles.readMoreButton}>Leer Más</button>
          </div>
          <div className={styles.newsItem}>
            <h3>Título de la Noticia 2</h3>
            <p>Descripción de la Noticia 2.</p>
            <button className={styles.readMoreButton}>Leer Más</button>
          </div>
          {/* Add more latest news items here */}
        </section>
      </main>
      <footer className={styles.footer}>
        {/* Add footer content here */}
      </footer>
    </div>
  );
}
