# Contribuindo com o Atlas

O desenvolvimento vigente ocorre em `current/atlas-web/`. Antes de propor uma
mudança, leia `handoff/DECISION_REGISTER.md` e preserve SQLite como fonte
canônica.

## Verificação local

```powershell
cd current/atlas-web
npm ci
npm run verify
python scripts/validate_links.py
```

Mudanças de conteúdo devem preservar Statement → Claim → Evidence → Source.
Novos tipos raiz, predicates ou mudanças de arquitetura exigem change control.
Nunca versione credenciais, exports privados do Zotero/Heurist ou mídia sem
licença e crédito verificáveis.
