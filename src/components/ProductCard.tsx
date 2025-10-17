import { Product } from '@/types/product';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Trash2, TrendingDown } from 'lucide-react';

interface ProductCardProps {
  product: Product;
  onDelete: (id: string) => void;
}

export const ProductCard = ({ product, onDelete }: ProductCardProps) => {
  const discountText = product.discount > 0 ? `-${product.discount}%` : 'Sin descuento';
  
  return (
    <Card className={product.isSpectacularDeal ? 'border-primary shadow-lg' : ''}>
      <CardHeader className="space-y-2">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-lg leading-tight">{product.name}</CardTitle>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(product.id)}
            className="shrink-0"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
        {product.isSpectacularDeal && (
          <Badge variant="destructive" className="w-fit">
            🔥 ¡Oferta Espectacular!
          </Badge>
        )}
      </CardHeader>
      
      <CardContent className="space-y-4">
        <div className="flex items-baseline gap-3">
          <span className="text-3xl font-bold">${product.currentPrice}</span>
          {product.originalPrice && product.originalPrice > product.currentPrice && (
            <span className="text-lg text-muted-foreground line-through">
              ${product.originalPrice}
            </span>
          )}
        </div>
        
        {product.discount > 0 && (
          <div className="flex items-center gap-2 text-sm text-primary">
            <TrendingDown className="h-4 w-4" />
            <span className="font-semibold">{discountText}</span>
          </div>
        )}
        
        <div className="text-xs text-muted-foreground">
          Actualizado: {new Date(product.lastUpdated).toLocaleString('es-ES')}
        </div>
        
        <Button asChild className="w-full" variant={product.isSpectacularDeal ? 'default' : 'outline'}>
          <a href={product.url} target="_blank" rel="noopener noreferrer">
            <ExternalLink className="mr-2 h-4 w-4" />
            Ver en ASUS Shop
          </a>
        </Button>
      </CardContent>
    </Card>
  );
};
