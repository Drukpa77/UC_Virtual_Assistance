import styles from './style.module.css'
export default function ChatAppBar() {
  return (
    <div className={styles['container']}>
      <div className={styles['version']}>UC Bot v1</div>
    </div>
  )
}