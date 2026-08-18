# Atlas — universo global de marcas automotivas

Baseline: 18 de agosto de 2026  
Estado: contrato editorial para expansão contínua  
Autoridade canônica: `current/atlas-web/data/atlas.sqlite`

## Objetivo

Transformar marcas em um dos eixos principais do Atlas. O universo deve incluir identidades
ativas e extintas, marcas absorvidas, fundidas, renomeadas, reativadas ou separadas, em todas
as regiões produtoras. A conclusão não será medida por uma promessa abstrata de “todas as
marcas que já existiram”, mas por um censo versionado, pesquisável e com critérios públicos.

## Unidade de registro

Uma **marca** é a identidade sob a qual um automóvel foi apresentado ou comercializado.
Ela não é automaticamente igual ao fabricante, à companhia proprietária, ao grupo econômico,
à fábrica ou à equipe de competição. Essas entidades permanecem separadas e são conectadas
por statements temporais.

Entram no censo:

- marcas que ofereceram ao menos um automóvel de passageiros em produção;
- marcas de competição que produziram automóveis indispensáveis à narrativa principal;
- marcas de ciclo curto, artesanais ou regionais com relevância histórica documentável;
- predecessoras e sucessoras necessárias para explicar genealogias;
- identidades relançadas, mesmo quando o novo negócio não conserva a empresa original.

Não entram automaticamente:

- nomes de versões, acabamentos, plataformas ou concessionárias;
- fabricantes de caminhões, ônibus e motocicletas sem automóvel de passageiro relacionado;
- fornecedores e carrozzerie que nunca comercializaram automóvel sob marca própria;
- projetos anunciados sem protótipo verificável ou atividade comercial demonstrável.

## Contrato mínimo por marca

Cada marca publicada deve possuir:

1. nome canônico, aliases e identificadores externos;
2. estado controlado: `active`, `discontinued`, `dormant`, `merged` ou `renamed`;
3. início e fim de atividade com precisão explícita;
4. país ou lugar de origem, sem confundir origem com mercados posteriores;
5. organização operadora e proprietário por intervalo, quando conhecidos;
6. predecessora, sucessora, fusão, cisão ou relançamento quando aplicável;
7. ao menos um automóvel de passageiros ou competição ligado por `marketed_under`;
8. ao menos um evento datado e três statements integralmente evidenciados;
9. narrativa em português e mídia licenciada;
10. nota de incerteza quando a continuidade da identidade for disputada.

## Relações de ciclo de vida

| Situação | Representação |
|---|---|
| Mudança de controle | `brand → owned_by → organization`, com validade temporal |
| Marca substituída | `nova marca → successor_of → marca anterior` |
| Empresa absorvida, marca mantida | novo `owned_by`; a entidade marca não é encerrada |
| Marca encerrada | `brand_status=discontinued` e evento de encerramento |
| Marca dormente | `brand_status=dormant`, sem inventar data definitiva de extinção |
| Relançamento com continuidade limitada | evento de revival e qualifier explicando a ruptura |
| Fusão que cria identidade nova | nova marca/organização ligada às predecessoras |
| Alteração apenas tipográfica | alias temporal; não criar nova marca |

## Ondas do censo

### M01 — fundadoras e pioneiras, 1886–1918

Benz, Daimler, Mercedes, Panhard & Levassor, De Dion-Bouton, Darracq, Mors, Clément-Bayard,
Rochet-Schneider, Napier, Wolseley, Austin, Humber, Vauxhall, Ford, Lincoln, Buick, Cadillac,
Oldsmobile, Packard, Peerless, Pierce-Arrow, Studebaker, REO, Maxwell, Rambler, Locomobile,
Fiat, Lancia, Itala, Isotta Fraschini, Alfa/ALFA, Hispano-Suiza, Laurin & Klement, Tatra e Opel.

### M02 — Europa: consolidação, luxo e marcas desaparecidas, 1919–1945

Morris, MG, Riley, Wolseley, Standard, Triumph, Rover, Singer, Hillman, Talbot, Sunbeam,
Alvis, Lagonda, Bentley, Aston Martin, SS/Jaguar, Delage, Delahaye, Voisin, Hotchkiss,
Salmson, Amilcar, Mathis, Rosengart, Simca, Panhard, Bugatti, BMW, DKW, Horch, Wanderer,
Adler, Maybach, Borgward, Hanomag, NSU, Steyr, Austro-Daimler, Praga, Aero e Jawa.

### M03 — Américas: escala, grupos e extinções

Chevrolet, Pontiac, Oakland, GMC apenas como contexto, LaSalle, Saturn, Hummer, Mercury,
Edsel, Continental, Chrysler, Plymouth, DeSoto, Dodge, Imperial, Eagle, Hudson, Nash,
AMC, Kaiser, Frazer, Willys, Jeep, Tucker, Cord, Auburn, Duesenberg, Graham, Studebaker,
Packard, Avanti, Tesla, Rivian, Lucid, Fisker, Karma, Saleen, Shelby, Vector e DeLorean;
no Canadá, McLaughlin e Acadian; no México, Mastretta e VUHL.

### M04 — Itália, esportivos, artesanais e carrozzerie-marcas

Ferrari, Maserati, Lamborghini, Abarth, Autobianchi, Innocenti, Iso, Bizzarrini, De Tomaso,
Pagani, Dallara, Cisitalia, OSCA, Siata, Moretti, ASA, Cizeta, Qvale, DR e marcas próprias
de carrozzerie somente quando houver automóvel comercializado sob identidade própria.

### M05 — Reino Unido e suas genealogias industriais

Lotus, McLaren, TVR, Bristol, Jensen, Reliant, Morgan, Caterham, Marcos, Noble, Ariel,
Ginetta, AC, Austin-Healey, Healey, Mini, Land Rover, Range Rover, Rolls-Royce, Bentley,
Vanden Plas, Princess e Daimler britânica, preservando as ambiguidades entre marca e empresa.

### M06 — Japão

Toyota, Toyopet, Lexus, Daihatsu, Hino como contexto, Nissan, Datsun, Infiniti, Prince,
Honda, Acura, Mazda, Mitsubishi, Subaru, Suzuki, Isuzu, Scion, Eunos, Autozam, Amati como
projeto não lançado, Mitsuoka, Tommykaira, Aspark e marcas históricas anteriores à guerra.

### M07 — Coreia, China e Taiwan

Hyundai, Genesis, Kia, Daewoo, SsangYong/KGM, Samsung/Renault Korea, Asia Motors, Proto,
Hongqi, SAIC, Roewe, MG contemporânea, Nanjing, Geely, Lynk & Co, Zeekr, Volvo sob controle
chinês sem reclassificar sua origem, Chery, Exeed, Jetour, Great Wall, Haval, Ora, Wey,
BYD, Denza, Yangwang, Fangchengbao, Nio, Onvo, Firefly, XPeng, Li Auto, Leapmotor, Xiaomi,
GAC, Aion, Dongfeng, Voyah, Changan, Avatr, JAC, BAIC, Arcfox, FAW, Bestune, Wuling,
Baojun, Seres, Aito, Luxgen e Yulon.

### M08 — Índia, Sudeste Asiático e Oriente Médio

Hindustan, Premier, Tata, Mahindra, Maruti Suzuki, Force, Standard India, Sipani, Reva,
DC/Avanti, VinFast, Proton, Perodua, Bufori, Thai Rung, Iran Khodro, Saipa, Pars Khodro,
Tofaş como fabricante/contexto, W Motors e marcas nacionais documentadas por produção.

### M09 — Europa Central, Oriental e União Soviética

Škoda, Tatra, Praga, Aero, Zastava, Yugo, Dacia, Oltcit, FSO, FSM, Polonez, Syrena,
Wartburg, Trabant, Sachsenring, Lada, Zhiguli, Moskvitch, GAZ, ZIL, UAZ como contexto,
ZAZ, LuAZ, IFA, Melkus, Rimac e marcas pós-socialistas ou relançadas.

### M10 — Escandinávia, Benelux, Espanha e Portugal

Volvo, Saab, Polestar, Koenigsegg, NEVS, Scania apenas contextual, Donkervoort, DAF,
Spyker, Minerva, Imperia, FN quando automóvel, SEAT, Cupra, Hispano-Suiza, Pegaso,
Santana, Tramontana, GTA/Spania, UMM, Portaro e Adamastor.

### M11 — América Latina

Gurgel, Puma, Miura, Santa Matilde, FNM, Troller, Lobini, Brasinca, Vemag como fabricante,
Willys do Brasil como organização, IKA, Torino como modelo e não marca, Siam Di Tella,
Pur Sang, Zanella quando automóvel, NSU-Fiat Argentina, Bessia, Anasagasti, Nordex como
fabricante, Grumett, Effa e outras identidades reconciliadas por país.

### M12 — Oceania e África

Holden, HSV, FPV, Bolwell, Elfin, Brabham Automotive, Leyland Australia, Rootes Australia,
Trekka, Hulme, Perana, GSM, Birkin, Optimal Energy/Joule, Mobius, Kiira, Innoson, Kantanka,
Laraki e Wallyscar, distinguindo produção, protótipo e montagem licenciada.

## Processo de inclusão

Cada onda começa em um registry de candidatos, passa por deduplicação de nomes, pesquisa
de fontes, reconciliação de organizações e veículos, importação idempotente, auditoria de
evidências e revisão visual. Uma marca só aparece como completa quando satisfaz o contrato
mínimo; candidatos permanecem no backlog e nunca são apresentados como fatos aprovados.

## Critério de conclusão

O censo terá uma versão anual fechada. Uma versão será considerada satisfatória quando:

- todos os candidatos conhecidos no registry tiverem decisão `published`, `context_only`,
  `duplicate`, `out_of_scope` ou `needs_research`;
- nenhuma marca publicada estiver sem automóvel, evento, fonte ou estado histórico;
- todas as relações de propriedade tiverem intervalo ou qualifier de precisão;
- cada região tiver revisão por fonte local ou especialista identificável;
- novas marcas possam ser adicionadas sem alterar o modelo canônico.

