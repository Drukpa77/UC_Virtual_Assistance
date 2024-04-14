export interface PayloadPacket {
  payload: Record<string, any>;
}

export const MESSAGE_BOT = 1;
export const MESSAGE_HUMAN = 0;