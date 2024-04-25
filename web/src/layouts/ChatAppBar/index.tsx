import styles from './style.module.css'
export default function ChatAppBar() {
  return (
    <div className={styles['container']}>
      <div className={styles['version']}>InfoOracle v1</div>
    </div>
  )
}