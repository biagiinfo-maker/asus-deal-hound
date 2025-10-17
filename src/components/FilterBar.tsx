import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search } from 'lucide-react';

interface FilterBarProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  filterType: string;
  onFilterChange: (value: string) => void;
}

export const FilterBar = ({ searchTerm, onSearchChange, filterType, onFilterChange }: FilterBarProps) => {
  return (
    <div className="flex flex-col sm:flex-row gap-4">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar productos..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-10"
        />
      </div>
      
      <Select value={filterType} onValueChange={onFilterChange}>
        <SelectTrigger className="w-full sm:w-[200px]">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Todos los productos</SelectItem>
          <SelectItem value="spectacular">Ofertas espectaculares</SelectItem>
          <SelectItem value="discount30">Descuento &gt; 30%</SelectItem>
          <SelectItem value="discount50">Descuento &gt; 50%</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
};
