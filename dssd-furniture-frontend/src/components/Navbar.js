// components/Navbar.js

import Link from 'next/link';
import { useRouter } from 'next/router'; // Import useRouter

import styles from '../styles/Navbar.module.css'; // Import your custom styles

export default function Navbar() {
  const router = useRouter(); // Initialize router

  const handleNavigation = (path) => {
    router.push(path); // Use router.push to navigate
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Link href="/">
          <div>Global Furniture</div>
        </Link>
      </div>
      <ul className={styles.navList}>
        <li>
          <div onClick={() => handleNavigation('/collection/create')} className={styles.navLink}>
            Crear Colección
          </div>
        </li>
        <li>
          <div onClick={() => handleNavigation('/collections')} className={styles.navLink}>
            Ver Colecciones
          </div>
        </li>
        {/* Add more navigation links as needed */}
      </ul>
    </nav>
  );
}