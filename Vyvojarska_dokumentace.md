# Vývojářská dokumentace

<p>Vstupní rastry jsou do programu dodány uživatelem přes příkazovou řádku. Využita je knihovna Argparse. Dva argumenty - rastry DMT a DMR jsou poté předány funkci run, která spustí běh programu. V této funkci probíhá porovnání souřadnicových systémů obou vstupních rastrů. Pokud se shodují běží program dále. Situace kdy rastry nejsou shodné, je řešena výjimkou. Další možné překážky jsou řešeny stanovením výjimek.
  
  Před samotnou analýzou rastrů je vykonána funkce intersect, která nachází průnik obou rastrů. Využíváme metodu intersection z knihovny Rasterio. Souřadnice hranic takového území ukládáme jako proměnné P1Y, P1X, P2Y, P2X, počítáme výšku a šířku průnikového okna a vytváříme matice těchto dvou rastrů nad průnikovým územím.
  
  Nakonec voláme funkci create_rasters, která prochází vstupní rastry po blocích. Pokud je rozdíl hodnot menší než stanovený treeshold, nabývá takový pixel v masce hodnoty 1, pokud nikoli, je hodnota stanovena jako nan. Využíváme k tomu funkci where z knihovny numpy. Za využití stejné funkce poté nahradíme v masce místa s hodnotou 1 hodnotou nadmořské výšky z DMT.
  
 Pomocí těchto nadmořských výšek poté s využitím funkce gradient z knihovny numpy počítáme sklony, které jsou ukládány do rastru slopes.tiff. Maska je ukládána jako mask.tiff
