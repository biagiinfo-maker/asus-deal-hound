export interface Product {
  id: string;
  name: string;
  url: string;
  currentPrice: number;
  originalPrice: number | null;
  discount: number;
  isSpectacularDeal: boolean;
  lastUpdated: string;
  priceHistory: PriceHistoryEntry[];
}

export interface PriceHistoryEntry {
  price: number;
  date: string;
}

export interface TelegramConfig {
  botToken: string;
  chatId: string;
  enabled: boolean;
}
