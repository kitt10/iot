### Smartblinds: Graphical User Interface
---

- Next.js
- React
- TypeScript
- Emotion

---

#### Development

Terminal 1 (backend):
```bash
$ cd engine
$ conda activate web
(web) $ python main.py
```

Terminal 2 (frontend):
```bash
$ cd gui
$ yarn dev
```

App: http://localhost:3000

---

#### Backend config (```engine/cfg_engine.yml```)

- GDrive
- Tornado can provide the web only if the Next.js app is exported to ```static_path_rel```
```yaml
webserver.host_web: true
webserver.static_path_rel: '../../gui/_static'
webserver.static_index: 'index.html'
```
otherwise
```yaml
webserver.host_web: false
```
and the web is provided with the Next.js server (```yarn```).

---

#### Frontend config (```gui/config.ts```)

- set up the backend connection
```typescript
//const engineURL = 'http://localhost'              // your local
const engineURL = ''                                // KKY PC IP
const enginePort = '9777'                           // take it from ../engine/cfg_engine.yml
```

