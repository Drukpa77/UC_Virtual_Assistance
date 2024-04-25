import { HTMLAttributes } from "react";

export interface FabWindowProps extends HTMLAttributes<HTMLDivElement> {
  onClose: () => void
}
