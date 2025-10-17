import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Download, Upload } from 'lucide-react';
import { storage } from '@/lib/storage';
import { toast } from '@/hooks/use-toast';

export const ImportExportDialog = () => {
  const [importData, setImportData] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const handleImport = () => {
    try {
      const count = storage.importData(importData);
      toast({
        title: 'Importación exitosa',
        description: `Se importaron ${count} productos`,
      });
      setImportData('');
      setIsOpen(false);
      window.location.reload();
    } catch (error) {
      toast({
        title: 'Error de importación',
        description: error instanceof Error ? error.message : 'Formato inválido',
        variant: 'destructive',
      });
    }
  };

  const handleExport = () => {
    const data = storage.exportData();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `asus-products-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    toast({
      title: 'Exportación exitosa',
      description: 'Archivo descargado',
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <Upload className="mr-2 h-4 w-4" />
          Importar/Exportar
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Gestionar Datos</DialogTitle>
        </DialogHeader>
        
        <Tabs defaultValue="import">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="import">Importar</TabsTrigger>
            <TabsTrigger value="export">Exportar</TabsTrigger>
          </TabsList>
          
          <TabsContent value="import" className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Pega el JSON generado por el script de scraping aquí:
            </p>
            <Textarea
              value={importData}
              onChange={(e) => setImportData(e.target.value)}
              placeholder='[{"id": "...", "name": "...", ...}]'
              rows={10}
              className="font-mono text-xs"
            />
            <Button onClick={handleImport} className="w-full">
              <Upload className="mr-2 h-4 w-4" />
              Importar Datos
            </Button>
          </TabsContent>
          
          <TabsContent value="export" className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Descarga todos los productos actuales en formato JSON:
            </p>
            <Button onClick={handleExport} className="w-full">
              <Download className="mr-2 h-4 w-4" />
              Descargar JSON
            </Button>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};
