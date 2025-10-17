import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Settings } from 'lucide-react';
import { storage } from '@/lib/storage';
import { toast } from '@/hooks/use-toast';

export const TelegramConfigDialog = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [config, setConfig] = useState(storage.getTelegramConfig());

  useEffect(() => {
    if (isOpen) {
      setConfig(storage.getTelegramConfig());
    }
  }, [isOpen]);

  const handleSave = () => {
    storage.saveTelegramConfig(config);
    toast({
      title: 'Configuración guardada',
      description: 'La configuración de Telegram se ha actualizado',
    });
    setIsOpen(false);
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <Settings className="mr-2 h-4 w-4" />
          Telegram
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Configuración de Telegram</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="botToken">Bot Token</Label>
            <Input
              id="botToken"
              type="password"
              value={config.botToken}
              onChange={(e) => setConfig({ ...config, botToken: e.target.value })}
              placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="chatId">Chat ID</Label>
            <Input
              id="chatId"
              value={config.chatId}
              onChange={(e) => setConfig({ ...config, chatId: e.target.value })}
              placeholder="-1001234567890"
            />
          </div>
          
          <div className="flex items-center justify-between">
            <Label htmlFor="enabled">Activar notificaciones</Label>
            <Switch
              id="enabled"
              checked={config.enabled}
              onCheckedChange={(enabled) => setConfig({ ...config, enabled })}
            />
          </div>
          
          <div className="rounded-lg bg-muted p-4 text-sm">
            <p className="font-semibold mb-2">Cómo obtener tus credenciales:</p>
            <ol className="list-decimal list-inside space-y-1 text-muted-foreground">
              <li>Crea un bot con @BotFather en Telegram</li>
              <li>Guarda el token que te proporciona</li>
              <li>Agrega el bot a tu chat o grupo</li>
              <li>Envía un mensaje y visita: api.telegram.org/bot[TOKEN]/getUpdates</li>
              <li>Copia el chat_id del JSON</li>
            </ol>
          </div>
          
          <Button onClick={handleSave} className="w-full">
            Guardar Configuración
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
