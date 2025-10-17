import { Product, TelegramConfig } from '@/types/product';

const PRODUCTS_KEY = 'asus_products';
const TELEGRAM_CONFIG_KEY = 'telegram_config';

export const storage = {
  getProducts: (): Product[] => {
    const data = localStorage.getItem(PRODUCTS_KEY);
    return data ? JSON.parse(data) : [];
  },

  saveProducts: (products: Product[]) => {
    localStorage.setItem(PRODUCTS_KEY, JSON.stringify(products));
  },

  addProduct: (product: Product) => {
    const products = storage.getProducts();
    const existingIndex = products.findIndex(p => p.url === product.url);
    
    if (existingIndex >= 0) {
      products[existingIndex] = product;
    } else {
      products.push(product);
    }
    
    storage.saveProducts(products);
  },

  deleteProduct: (id: string) => {
    const products = storage.getProducts().filter(p => p.id !== id);
    storage.saveProducts(products);
  },

  getTelegramConfig: (): TelegramConfig => {
    const data = localStorage.getItem(TELEGRAM_CONFIG_KEY);
    return data ? JSON.parse(data) : { botToken: '', chatId: '', enabled: false };
  },

  saveTelegramConfig: (config: TelegramConfig) => {
    localStorage.setItem(TELEGRAM_CONFIG_KEY, JSON.stringify(config));
  },

  importData: (jsonData: string): number => {
    try {
      const imported = JSON.parse(jsonData) as Product[];
      const current = storage.getProducts();
      
      imported.forEach(product => {
        const existing = current.find(p => p.url === product.url);
        if (existing) {
          product.priceHistory = [
            ...existing.priceHistory,
            ...product.priceHistory
          ].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        }
      });
      
      storage.saveProducts(imported);
      return imported.length;
    } catch (error) {
      throw new Error('Invalid JSON format');
    }
  },

  exportData: (): string => {
    return JSON.stringify(storage.getProducts(), null, 2);
  }
};
