import { HTMLAttributes } from "react";

export interface ChatMessageProps extends HTMLAttributes<HTMLDivElement> {
  message: React.ReactNode;
}
