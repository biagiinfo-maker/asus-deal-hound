import { useState, useEffect } from 'react';
import { storage } from '@/lib/storage';
import { Product } from '@/types/product';
import { ProductCard } from '@/components/ProductCard';
import { ImportExportDialog } from '@/components/ImportExportDialog';
import { TelegramConfigDialog } from '@/components/TelegramConfigDialog';
import { FilterBar } from '@/components/FilterBar';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';

const Index = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  useEffect(() => {
  const fetchProducts = async () => {
    try {
      // Pide al servidor el archivo que está en la carpeta 'public'
      const response = await fetch('/products.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("No se pudo cargar 'products.json'. ¿Ejecutaste el script?", error);
      // Como respaldo, intentamos cargar desde el almacenamiento local
      setProducts(storage.getProducts());
    }
  };
  
  fetchProducts();
}, []);

  const loadProducts = async () => {
  try {
    // Añade un timestamp para evitar que el navegador use una versión en caché del archivo
    const response = await fetch(`/products.json?v=${new Date().getTime()}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    setProducts(data);
  } catch (error) {
    console.error("No se pudo recargar 'products.json'.", error);
  }
};

  const handleDelete = (id: string) => {
    storage.deleteProduct(id);
    loadProducts();
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    switch (filterType) {
      case 'spectacular':
        return matchesSearch && product.isSpectacularDeal;
      case 'discount30':
        return matchesSearch && product.discount >= 30;
      case 'discount50':
        return matchesSearch && product.discount >= 50;
      default:
        return matchesSearch;
    }
  });

  const spectacularCount = products.filter(p => p.isSpectacularDeal).length;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">ASUS Deal Hound 🔍</h1>
              <p className="text-muted-foreground">
                Rastreador de ofertas de ASUS Shop
              </p>
            </div>
            
            <div className="flex gap-2 flex-wrap">
              <TelegramConfigDialog />
              <ImportExportDialog />
              <Button onClick={() => loadProducts()} variant="outline">
                <RefreshCw className="mr-2 h-4 w-4" />
                Recargar
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div className="flex gap-4 text-sm">
            <div className="rounded-lg bg-muted px-4 py-2">
              <span className="font-semibold">{products.length}</span> productos
            </div>
            {spectacularCount > 0 && (
              <div className="rounded-lg bg-primary/10 px-4 py-2 text-primary">
                <span className="font-semibold">{spectacularCount}</span> ofertas espectaculares
              </div>
            )}
          </div>
        </div>

        <div className="mb-6">
          <FilterBar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            filterType={filterType}
            onFilterChange={setFilterType}
          />
        </div>

        {filteredProducts.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📦</div>
            <h3 className="text-2xl font-semibold mb-2">No hay productos</h3>
            <p className="text-muted-foreground mb-6">
              {products.length === 0 
                ? 'Importa datos desde el script de scraping para comenzar'
                : 'No se encontraron productos con los filtros actuales'}
            </p>
            <ImportExportDialog />
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredProducts.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </main>

      <footer className="border-t mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>Ejecuta el script de Python localmente para actualizar los datos</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
