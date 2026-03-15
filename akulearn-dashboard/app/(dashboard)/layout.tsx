import Link from "next/link";
import Image from "next/image";
import styles from "../mainNav.module.css";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <nav className={styles.mainNav}>
        <Link href="/">
          <Image src="/akudemy-logo.svg" alt="Akudemy Logo" width={120} height={32} style={{ verticalAlign: "middle" }} />
        </Link>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/notifications">Notifications</Link>
        <Link href="/profile">Profile</Link>
      </nav>
      {children}
    </>
  );
}
