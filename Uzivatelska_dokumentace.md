# Uživatelská dokumentace

<p>Do rukou se Vám dostal program, který zpracovává digitální model terénu a digitální model reliéfu. Na základě těchto dat nalezne nezastavěné plochy a určí na nich 
  sklon.
  
  Uživatel vkládá do programu DMT a DMR přes příkazovou řádku v rastrovém formátu .tiff.
  Tento program nejprve vyhodnotí rozdíl nadmořských výšek DMT a DMR. V místech, kde je rozdíl menší než 1 metr, následně vypočítá sklon. Tento sklon je uložen jako rastr pod názvem slopes.tiff.
  Při běhu programu je uložena také maska míst bez zástavby (viz výše) pod názvem mask.tiff.
  
  Při zpracování dat program napřed ověří, že oba vstupní soubory mají stejný souřadnicový systém. Pokud ne, uživatel je upozorněn.
  
  Při běhu programu je vytvořen průnik obou rastrů. Nad tímto průnikem poté probíhají výpočty, které jsou prováděny po menších částech území. Tento postup je volen s ohledem na výpočetní kapacitu běžných zařízení.
