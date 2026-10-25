# Instrucciones para agentes de IA

Lee [`README.md`](README.md) completo (sobre todo «Si eres una IA: empieza aquí») y [`manifiesto.md`](manifiesto.md) antes de
escribir un manifiesto. Para animaciones, [`cli/animaciones/README.md`](cli/animaciones/README.md).

Reglas cortas:
- Entrega manifiestos para revisar en el editor; renderiza solo con aprobación.
- Corre `cli/revisar-voz.py` antes de proponer cortes de voz y `cli/revisar-entrega.py` antes de dar un render por bueno.
- Cambia solo lo que te pidan; no borres piezas aprobadas ni agregues funciones que nadie pidió.
- Tras tocar código: `npm run build`; si tocaste `src/lib/graph.ts`, renderiza `ejemplo/manifiesto.json`.
