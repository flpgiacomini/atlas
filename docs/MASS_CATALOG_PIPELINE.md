# Pipeline catalográfico em massa

O Atlas separa cobertura catalográfica de profundidade editorial. Um registro pode ser encontrado no site antes de receber narrativa e claims históricos, desde que sua origem seja atribuída e seu nível seja exibido claramente.

## Níveis

- `catalog`: identidade mínima, fonte catalográfica, pontuação e fila de promoção.
- `editorial`: descrição contextual, relações, evidências e mídia licenciada.
- `dossier`: cobertura aprofundada com múltiplas fontes e documentação.

Registros legados sem `editorial_level` são tratados como `editorial`; o importador MASS01 grava o nível explicitamente em todo o banco.

## Comandos

```powershell
cd current/atlas-web
npm.cmd run catalog:import
npm.cmd run atlas:sync
```

`catalog:import` é idempotente: UUIDs e identificadores externos são determinísticos, registros existentes são atualizados sem duplicação e colisões de nomes entre tipos permanecem entidades separadas.

`atlas:sync` importa, valida a política de fontes, regenera as projeções e deixa o SQLite como única autoridade publicada.

## Política de fontes

`data/source-trust.registry.json` define, por fonte, campos permitidos, confiança, modo de uso e situação de licença. AllCarIndex, Auto-Data e Ultimatecarpage permanecem fontes de descoberta ou conferência até haver autorização suficiente para republicação em massa. Seus dados não criam automaticamente claims aceitos.

## Promoção

Um registro `catalog` somente passa a `editorial` quando possui:

1. identidade reconciliada;
2. fonte individual adequada;
3. descrição contextual;
4. relações relevantes com claims e evidências;
5. mídia licenciada quando publicada visualmente.

O lote MASS01 usa os registros autorais de curadoria do próprio Atlas e pode, portanto, ser versionado integralmente.

## Verificação progressiva

Lotes `Rxx` enriquecem candidatos prioritários sem alterar automaticamente seu nível editorial. Um registro com `verification_state=source_backed` pode exibir narrativa, relações e a fonte vinculada, mas continua identificado como catálogo até satisfazer todos os critérios de promoção. O primeiro lote é executado por `npm run catalog:enrich:r01` e integra o comando `atlas:sync`.
