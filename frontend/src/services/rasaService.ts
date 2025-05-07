import { RasaResponse } from '../types/chat';

const RASA_API_URL = 'http://localhost:5005'; // Change this to your Rasa server URL

export const sendMessageToRasa = async (
  message: string,
  senderId: string = 'default'
): Promise<RasaResponse[]> => {
  try {
    const response = await fetch(`${RASA_API_URL}/webhooks/rest/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sender: senderId,
        message,
      }),
    });

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message to Rasa:', error);
    throw error;
  }
};