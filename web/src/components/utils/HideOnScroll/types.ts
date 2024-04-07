import { ReactNode } from "react"

export interface ScrollProps {
  direction: 'up' | 'down' | 'left' | 'right'
  children: ReactNode
}