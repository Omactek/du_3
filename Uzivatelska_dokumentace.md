# Uživatelská dokumentace

<p>Do rukou se Vám dostal program, který zpracovává digitální model terénu a digitální model reliéfu. Na základě těchto dat nalezne nezastavěné plochy a určí na nich 
  sklon.
  Uživatel vkládá do programu DMT a DMR přes příkazovou řádku v rastrovém formátu .tiff.
  Tento program nejprve vyhodnotí rozdíl nadmořských výšek DMT a DMR. V místech, kde je rozdíl menší než 1 metr následně vyhodnotí sklon. Tento sklon je uložen jako rastr
  pod názvem slopes.tiff.
  Při běhu programu je uložena také maska míst bez zástavby (viz výše) pod názvem mask.tiff.
