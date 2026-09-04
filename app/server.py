import os, sys, json, time, secrets, hashlib, hmac, shutil, threading, webbrowser, traceback
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from http.cookies import SimpleCookie
from pathlib import Path

APP_VERSION = '2.5.1'
PORT = int(os.environ.get('PORT', '8972'))
PUBLIC_PORT = int(os.environ.get('PUBLIC_PORT', '8973'))
HOST = os.environ.get('HOST', '0.0.0.0')

# Program dosyaları ile canlı işletme verisini birbirinden ayır.
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).resolve().parent
    RESOURCE_DIR = Path(getattr(sys, '_MEIPASS', APP_DIR))
else:
    APP_DIR = Path(__file__).resolve().parent
    RESOURCE_DIR = APP_DIR

# Windows'ta tüm sürümler aynı sabit kullanıcı veri klasörünü kullanır.
# Böylece kurulum/güncelleme EXE dosyalarını değiştirse bile servis, kasa, kullanıcı ve ayarlar korunur.
_local_appdata = os.environ.get('LOCALAPPDATA')
if _local_appdata:
    USER_DATA_DIR = Path(_local_appdata) / 'TeknikServisPro' / 'Data'
else:
    USER_DATA_DIR = Path.home() / '.teknikservispro' / 'data'

DB_FILE = USER_DATA_DIR / 'db.json'
BACKUP_DIR = USER_DATA_DIR / 'backups'
LOG_DIR = USER_DATA_DIR / 'logs'
STATIC_DIR = RESOURCE_DIR if getattr(sys, 'frozen', False) else APP_DIR
INDEX_FILE = STATIC_DIR / 'index.html'
LEGACY_DB_FILE = APP_DIR / 'db.json'
SEED_DB_FILE = RESOURCE_DIR / 'db.json'
SESSIONS = {}
SESSION_TTL = 12 * 60 * 60
_STORAGE_READY = False


def empty_db():
    return {
        'version': 2.51,
        'serviceRecords': [], 'customers': [], 'devices': [], 'cashRecords': [], 'inventory': [], 'users': [],
        'settings': {
            'businessName': 'Sistem Bilgisayar Teknik Destek',
            'businessSubtitle': 'Bilgisayar & Donanım Onarım Servisi',
            'phone': '', 'email': '', 'address': '', 'taxOffice': '', 'taxNo': '',
            'defaultWarrantyDays': 90, 'logo': '', 'theme': 'blue'
        }
    }


def _read_db_candidate(path):
    try:
        raw = json.loads(path.read_text(encoding='utf-8-sig'))
        return raw if isinstance(raw, (dict, list)) else None
    except Exception:
        return None


def _data_score(raw):
    """Gerçek işletme verisini boş/seed DB'den ayırmak için kaba puan."""
    if isinstance(raw, list):
        return len(raw) * 100
    if not isinstance(raw, dict):
        return -1
    return (
        len(raw.get('serviceRecords') or []) * 100
        + len(raw.get('cashRecords') or []) * 20
        + len(raw.get('inventory') or []) * 10
        + len(raw.get('customers') or []) * 15
        + len(raw.get('devices') or []) * 15
        + len(raw.get('users') or [])
    )


def _merge_users_if_needed(recovered, current):
    if not isinstance(recovered, dict) or not isinstance(current, dict):
        return recovered
    if not recovered.get('users') and current.get('users'):
        recovered = dict(recovered)
        recovered['users'] = current['users']
    return recovered


def ensure_storage():
    global _STORAGE_READY
    if _STORAGE_READY:
        return

    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f'Arayüz dosyası bulunamadı: {INDEX_FILE}')

    # Migration/kurtarma yalnızca süreç başlarken bir kez yapılır.
    # Normal veri okuma/yazmada eski dosyalar tekrar karşılaştırılmaz;
    # böylece geri yüklenen veya sonradan değiştirilen canlı DB'nin üstüne yazılamaz.
    current_raw = _read_db_candidate(DB_FILE) if DB_FILE.exists() else None
    current_score = _data_score(current_raw)

    legacy_candidates = []
    for candidate in (LEGACY_DB_FILE, APP_DIR / 'data' / 'db.json'):
        if candidate.exists() and candidate.resolve() != DB_FILE.resolve():
            legacy_candidates.append(candidate)
    old_backup_dir = APP_DIR / 'backups'
    if old_backup_dir.exists():
        legacy_candidates.extend(sorted(old_backup_dir.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True))

    # Yalnızca canlı DB yoksa veya gerçekten boşsa eski gerçek veriyi kurtar.
    if current_score <= 0:
        best_path = None
        best_raw = None
        best_score = current_score
        for candidate in legacy_candidates:
            raw = _read_db_candidate(candidate)
            score = _data_score(raw)
            if score > best_score:
                best_path, best_raw, best_score = candidate, raw, score
        if best_path is not None and best_raw is not None:
            if DB_FILE.exists():
                try:
                    rescue = BACKUP_DIR / f'pre_recovery_{time.strftime("%Y-%m-%dT%H-%M-%S")}.json'
                    shutil.copy2(DB_FILE, rescue)
                except OSError:
                    pass
            best_raw = _merge_users_if_needed(best_raw, current_raw)
            DB_FILE.write_text(json.dumps(best_raw, ensure_ascii=False, indent=2), encoding='utf-8')
            current_raw = best_raw

    if not DB_FILE.exists():
        seed = _read_db_candidate(SEED_DB_FILE) if SEED_DB_FILE.exists() else None
        DB_FILE.write_text(json.dumps(seed if seed is not None else empty_db(), ensure_ascii=False, indent=2), encoding='utf-8')

    _STORAGE_READY = True


def normalize_db(raw):
    base = empty_db()
    if isinstance(raw, list):
        base['serviceRecords'] = raw
        return base
    raw = raw if isinstance(raw, dict) else {}
    out = {**base, **raw}
    for key in ('serviceRecords', 'customers', 'devices', 'cashRecords', 'inventory', 'users'):
        out[key] = raw.get(key) if isinstance(raw.get(key), list) else []
    settings = raw.get('settings') if isinstance(raw.get('settings'), dict) else {}
    out['settings'] = {**base['settings'], **settings}
    return out


def read_db():
    ensure_storage()
    db=normalize_db(json.loads(DB_FILE.read_text(encoding='utf-8-sig')))
    changed=False
    for rec in db.get('serviceRecords') or []:
        if not rec.get('portalToken'):
            rec['portalToken']=secrets.token_urlsafe(24); changed=True
    if changed: write_db(db)
    return db


def write_db(data):
    ensure_storage()
    normalized = normalize_db(data)
    normalized['version'] = 2.51
    for rec in normalized.get('serviceRecords') or []:
        if not rec.get('portalToken'):
            rec['portalToken'] = secrets.token_urlsafe(24)
    temp = DB_FILE.with_suffix('.json.tmp')
    payload = json.dumps(normalized, ensure_ascii=False, indent=2)
    with temp.open('w', encoding='utf-8') as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, DB_FILE)
    return normalized


def db_summary(db):
    return {
        'serviceCount': len(db.get('serviceRecords') or []),
        'customerCount': len(db.get('customers') or []),
        'deviceCount': len(db.get('devices') or []),
        'cashCount': len(db.get('cashRecords') or []),
        'inventoryCount': len(db.get('inventory') or []),
        'dataFile': str(DB_FILE),
        'dataFileExists': DB_FILE.exists(),
        'dataFileSize': DB_FILE.stat().st_size if DB_FILE.exists() else 0,
    }


def backup_current_db():
    if not DB_FILE.exists(): return
    stamp = time.strftime('%Y-%m-%dT%H-%M-%S')
    dest = BACKUP_DIR / f'db_{stamp}.json'
    try:
        shutil.copy2(DB_FILE, dest)
        files = sorted(BACKUP_DIR.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        for p in files[20:]:
            try: p.unlink()
            except OSError: pass
    except OSError: pass


def hash_password(password, salt_hex=None):
    salt_hex = salt_hex or secrets.token_hex(16)
    salt = bytes.fromhex(salt_hex)
    # Node crypto.scryptSync varsayılanlarıyla uyumlu.
    digest = hashlib.scrypt(str(password).encode('utf-8'), salt=salt, n=16384, r=8, p=1, dklen=64)
    return f'{salt_hex}:{digest.hex()}'


def verify_password(password, stored=''):
    try:
        salt_hex, expected_hex = str(stored).split(':', 1)
        actual = hash_password(password, salt_hex).split(':', 1)[1]
        return hmac.compare_digest(actual, expected_hex)
    except Exception:
        return False


def safe_user(u):
    return {k: v for k, v in u.items() if k != 'passwordHash'}


def cleanup_sessions():
    now = time.time()
    for token in list(SESSIONS):
        if SESSIONS[token]['expires'] < now: SESSIONS.pop(token, None)


def session_user(headers):
    cleanup_sessions()
    cookie = SimpleCookie()
    try: cookie.load(headers.get('Cookie', ''))
    except Exception: return None
    morsel = cookie.get('tsp_session')
    if not morsel: return None
    token = morsel.value
    session = SESSIONS.get(token)
    if not session: return None
    session['expires'] = time.time() + SESSION_TTL
    return session['user']


def new_session(user):
    token = secrets.token_hex(32)
    clean = {k: user.get(k) for k in ('id', 'name', 'username', 'role')}
    SESSIONS[token] = {'user': clean, 'expires': time.time() + SESSION_TTL}
    return token, clean


def _norm_phone(value):
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _portal_service_by_token(db, token):
    token = str(token or '').strip()
    if len(token) < 20: return None
    for rec in db.get('serviceRecords') or []:
        if hmac.compare_digest(str(rec.get('portalToken') or ''), token): return rec
    return None

def _portal_service(db, service_no, phone):
    wanted_no = str(service_no or "").strip().casefold()
    wanted_phone = _norm_phone(phone)
    if not wanted_no or len(wanted_phone) < 7:
        return None
    for rec in db.get("serviceRecords") or []:
        if str(rec.get("serviceNo","")).strip().casefold() == wanted_no and _norm_phone(rec.get("customerPhone")) == wanted_phone:
            return rec
    return None


def _public_service(rec, settings):
    offers=[]
    for o in rec.get("offers") or []:
        offers.append({k:o.get(k) for k in ("id","version","amount","note","status","createdAt","decidedAt")})
    history=[]
    for h in rec.get("history") or []:
        if h.get("visibility") == "internal":
            continue
        history.append({"date":h.get("date"),"text":h.get("text") or h.get("title") or "","type":h.get("type","activity"),"actor":h.get("actor","Servis")})
    return {"business":{"name":settings.get("businessName","Teknik Servis Pro"),"phone":settings.get("phone",""),"email":settings.get("email","")},"serviceNo":rec.get("serviceNo"),"customerName":rec.get("customerName"),"deviceType":rec.get("deviceType"),"deviceModel":rec.get("deviceModel"),"serialNo":rec.get("serialNo"),"complaint":rec.get("complaint"),"status":rec.get("status"),"entryDate":rec.get("entryDate"),"estimatedDate":rec.get("estimatedDate"),"warrantyUntil":rec.get("warrantyUntil"),"totalFee":rec.get("totalFee",0),"paidAmount":rec.get("paidAmount",0),"offers":offers,"history":history}


class Handler(SimpleHTTPRequestHandler):
    server_version = 'TeknikServisPro/2.5.1'

    def log_message(self, fmt, *args):
        try:
            with (LOG_DIR / 'access.log').open('a', encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {self.address_string()} {fmt % args}\n")
        except Exception: pass

    def end_headers(self):
        # Mobil tarayıcı/Tailscale erişiminde eski HTML/JS önbellekten gelmesin.
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def translate_path(self, path):
        # Statik dosyaları yalnızca paketlenmiş arayüz klasöründen sun.
        path = urlparse(path).path.lstrip('/') or 'index.html'
        target = (STATIC_DIR / path).resolve()
        try: target.relative_to(STATIC_DIR.resolve())
        except ValueError: return str(STATIC_DIR / '__forbidden__')
        return str(target)

    def send_json(self, obj, status=200, headers=None):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in (headers or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)

    def read_json(self):
        length = int(self.headers.get('Content-Length', '0') or 0)
        if length > 12 * 1024 * 1024: raise ValueError('İstek çok büyük')
        raw = self.rfile.read(length) if length else b'{}'
        return json.loads(raw.decode('utf-8') or '{}')

    def auth(self, admin=False):
        u = session_user(self.headers)
        if not u:
            self.send_json({'error': 'Oturum gerekli'}, 401); return None
        if admin and u.get('role') != 'Yönetici':
            self.send_json({'error': 'Yönetici yetkisi gerekli'}, 403); return None
        return u

    def do_GET(self):
        p = urlparse(self.path).path
        try:
            if p == '/api/health': return self.send_json({'ok': True, 'version': APP_VERSION, 'runtime': 'python'})
            if p == '/api/diagnostics':
                if not self.auth(): return
                db = read_db()
                info = db_summary(db)
                info.update({'ok': True, 'version': APP_VERSION, 'pid': os.getpid(), 'appDir': str(APP_DIR)})
                return self.send_json(info)
            if p == '/api/auth/status':
                db = read_db(); u = session_user(self.headers)
                return self.send_json({'setupRequired': len(db['users']) == 0, 'authenticated': bool(u), 'user': u})
            if p == '/api/users':
                if not self.auth(admin=True): return
                return self.send_json([safe_user(x) for x in read_db()['users']])
            if p == '/api/portal':
                q = parse_qs(urlparse(self.path).query); db = read_db()
                token=(q.get('token') or [''])[0]
                rec = _portal_service_by_token(db, token) if token else _portal_service(db, (q.get('serviceNo') or [''])[0], (q.get('phone') or [''])[0])
                if not rec: return self.send_json({'error':'Servis kaydı bulunamadı veya bağlantı geçersiz.'},404)
                if not rec.get('portalToken'):
                    rec['portalToken']=secrets.token_urlsafe(24); write_db(db)
                return self.send_json({'success':True, 'service':_public_service(rec, db.get('settings') or {}), 'portalToken':rec.get('portalToken')})
            if p == '/api/data':
                if not self.auth(): return
                db = read_db(); db.pop('users', None)
                return self.send_json(db)
            if p.startswith('/api/'):
                return self.send_json({'error': 'Bulunamadı'}, 404)
            return super().do_GET()
        except Exception as e:
            log_exception(e); return self.send_json({'error': 'Sunucu hatası'}, 500)

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            if p == '/api/shutdown':
                if self.client_address[0] not in ('127.0.0.1', '::1'):
                    return self.send_json({'error': 'Yetkisiz'}, 403)
                self.send_json({'success': True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            body = self.read_json()
            if p == '/api/auth/setup':
                db = read_db()
                if db['users']: return self.send_json({'error': 'İlk kurulum tamamlanmış'}, 409)
                name = str(body.get('name','')).strip(); username = str(body.get('username','')).strip(); password = str(body.get('password',''))
                if not name or len(username) < 3 or len(password) < 6:
                    return self.send_json({'error': 'Ad, en az 3 karakter kullanıcı adı ve en az 6 karakter şifre gerekli'}, 400)
                user = {'id': int(time.time()*1000), 'name': name, 'username': username, 'role': 'Yönetici', 'active': True,
                        'passwordHash': hash_password(password), 'createdAt': time.strftime('%Y-%m-%dT%H:%M:%S')}
                db['users'].append(user); backup_current_db(); write_db(db)
                token, clean = new_session(user)
                return self.send_json({'success': True, 'user': clean}, headers={'Set-Cookie': f'tsp_session={token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=43200'})
            if p == '/api/auth/login':
                db = read_db(); username = str(body.get('username','')).strip().casefold()
                user = next((x for x in db['users'] if x.get('active',True) is not False and str(x.get('username','')).casefold()==username), None)
                if not user or not verify_password(body.get('password',''), user.get('passwordHash','')):
                    return self.send_json({'error': 'Kullanıcı adı veya şifre hatalı'}, 401)
                token, clean = new_session(user)
                return self.send_json({'success': True, 'user': clean}, headers={'Set-Cookie': f'tsp_session={token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=43200'})
            if p == '/api/auth/logout':
                cookie = SimpleCookie(); cookie.load(self.headers.get('Cookie',''))
                if cookie.get('tsp_session'): SESSIONS.pop(cookie['tsp_session'].value, None)
                return self.send_json({'success': True}, headers={'Set-Cookie':'tsp_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0'})
            if p == '/api/auth/change-password':
                current = self.auth()
                if not current: return
                db = read_db(); user = next((x for x in db['users'] if x.get('id')==current.get('id')), None)
                if not user or not verify_password(body.get('currentPassword',''), user.get('passwordHash','')):
                    return self.send_json({'error':'Mevcut şifre yanlış'},400)
                np = str(body.get('newPassword',''))
                if len(np)<6: return self.send_json({'error':'Yeni şifre en az 6 karakter olmalı'},400)
                user['passwordHash']=hash_password(np); backup_current_db(); write_db(db)
                return self.send_json({'success':True})
            if p == '/api/users':
                if not self.auth(admin=True): return
                db=read_db(); name=str(body.get('name','')).strip(); username=str(body.get('username','')).strip(); password=str(body.get('password',''))
                role=body.get('role') if body.get('role') in ('Yönetici','Teknisyen','Kasa') else 'Teknisyen'
                if not name or len(username)<3 or len(password)<6: return self.send_json({'error':'Bilgileri kontrol edin; şifre en az 6 karakter olmalı'},400)
                if any(str(x.get('username','')).casefold()==username.casefold() for x in db['users']): return self.send_json({'error':'Bu kullanıcı adı zaten kullanılıyor'},409)
                db['users'].append({'id':int(time.time()*1000),'name':name,'username':username,'role':role,'active':True,'passwordHash':hash_password(password),'createdAt':time.strftime('%Y-%m-%dT%H:%M:%S')})
                backup_current_db(); write_db(db); return self.send_json({'success':True})
            if p == '/api/portal/decision':
                db = read_db()
                rec = _portal_service_by_token(db, body.get('token')) if body.get('token') else _portal_service(db, body.get('serviceNo'), body.get('phone'))
                if not rec: return self.send_json({'error':'Servis kaydı bulunamadı'},404)
                offers = rec.get('offers') if isinstance(rec.get('offers'), list) else []
                offer = next((x for x in offers if str(x.get('id')) == str(body.get('offerId'))), None)
                if not offer: return self.send_json({'error':'Teklif bulunamadı'},404)
                if offer.get('status') != 'Onay Bekliyor': return self.send_json({'error':'Bu teklif daha önce sonuçlandırılmış'},409)
                decision = str(body.get('decision','')).lower()
                if decision not in ('approve','reject'): return self.send_json({'error':'Geçersiz karar'},400)
                now = time.strftime('%Y-%m-%dT%H:%M:%S')
                if decision == 'approve':
                    offer['status']='Onaylandı'; rec['status']='İşlemde'; text=f"Teklif v{offer.get('version','')} müşteri portalından onaylandı · {offer.get('amount',0)} TL"
                else:
                    offer['status']='Reddedildi'; rec['status']='Arıza Tespit'; text=f"Teklif v{offer.get('version','')} müşteri portalından reddedildi"
                offer['decidedAt']=now; offer['decisionSource']='Müşteri Portalı'
                rec['history'] = rec.get('history') if isinstance(rec.get('history'), list) else []
                rec['history'].append({'date':now,'text':text,'type':'offer','actor':'Müşteri Portalı','visibility':'customer'})
                backup_current_db(); write_db(db)
                return self.send_json({'success':True,'service':_public_service(rec, db.get('settings') or {})})
            if p == '/api/backup/restore':
                if not self.auth(): return
                current = read_db()
                restored = normalize_db(body)
                restored['users'] = current['users']
                expected = db_summary(restored)
                backup_current_db()
                write_db(restored)
                verified = read_db()
                actual = db_summary(verified)
                if (actual['serviceCount'] != expected['serviceCount'] or
                    actual['cashCount'] != expected['cashCount'] or
                    actual['inventoryCount'] != expected['inventoryCount'] or
                    actual['customerCount'] != expected['customerCount'] or
                    actual['deviceCount'] != expected['deviceCount']):
                    return self.send_json({'error':'Geri yükleme disk doğrulaması başarısız', 'expected':expected, 'actual':actual},500)
                return self.send_json({'success':True, **actual})
            if p == '/api/data':
                if not self.auth(): return
                current=read_db(); nextdb=normalize_db(body); nextdb['users']=current['users']; backup_current_db(); write_db(nextdb)
                verified = read_db()
                return self.send_json({'success':True, **db_summary(verified)})
            return self.send_json({'error':'Bulunamadı'},404)
        except Exception as e:
            log_exception(e); return self.send_json({'error':'Sunucu hatası'},500)

    def do_PATCH(self):
        p=urlparse(self.path).path
        try:
            if not p.startswith('/api/users/'):
                return self.send_json({'error':'Bulunamadı'},404)
            current=self.auth(admin=True)
            if not current: return
            user_id=p.rsplit('/',1)[-1]; body=self.read_json(); db=read_db()
            user=next((x for x in db['users'] if str(x.get('id'))==user_id),None)
            if not user: return self.send_json({'error':'Kullanıcı bulunamadı'},404)
            if user.get('id')==current.get('id') and body.get('active') is False: return self.send_json({'error':'Kendi hesabınızı pasif yapamazsınız'},400)
            if body.get('name') is not None: user['name']=str(body['name']).strip() or user.get('name')
            if body.get('role') in ('Yönetici','Teknisyen','Kasa'): user['role']=body['role']
            if body.get('active') is not None: user['active']=bool(body['active'])
            if len(str(body.get('password','')))>=6: user['passwordHash']=hash_password(body['password'])
            backup_current_db(); write_db(db); return self.send_json({'success':True})
        except Exception as e:
            log_exception(e); return self.send_json({'error':'Sunucu hatası'},500)


class PublicPortalHandler(Handler):
    """Internet tüneline yalnız müşteri portalını açar; yönetim paneli/API kapalıdır."""
    def translate_path(self, path):
        p=urlparse(path).path
        if p in ('/','/portal.html'):
            return str(STATIC_DIR / 'portal.html')
        return str(STATIC_DIR / '__forbidden__')
    def do_GET(self):
        p=urlparse(self.path).path
        if p == '/api/health': return self.send_json({'ok':True,'version':APP_VERSION,'portalOnly':True})
        if p == '/api/portal': return super().do_GET()
        if p in ('/','/portal.html'): return SimpleHTTPRequestHandler.do_GET(self)
        return self.send_json({'error':'Bu bağlantıda yalnız müşteri portalı kullanılabilir.'},403)
    def do_POST(self):
        if urlparse(self.path).path == '/api/portal/decision': return super().do_POST()
        return self.send_json({'error':'Bu bağlantıda yalnız müşteri portalı kullanılabilir.'},403)
    def do_PATCH(self):
        return self.send_json({'error':'Yetkisiz'},403)


def log_exception(exc):
    ensure_storage()
    try:
        with (LOG_DIR/'server-error.log').open('a', encoding='utf-8') as f:
            f.write('\n' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            traceback.print_exception(type(exc), exc, exc.__traceback__, file=f)
    except Exception: pass


def open_browser_later():
    time.sleep(0.7)
    try: webbrowser.open(f'http://127.0.0.1:{PORT}', new=1)
    except Exception as e: log_exception(e)


def port_already_running():
    import urllib.request
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/api/health', timeout=0.7) as r:
            return r.status == 200
    except Exception: return False


def main():
    ensure_storage()
    if port_already_running():
        webbrowser.open(f'http://127.0.0.1:{PORT}', new=1); return
    try:
        server=ThreadingHTTPServer((HOST, PORT), Handler); server.daemon_threads = True
        public_server=ThreadingHTTPServer(('127.0.0.1', PUBLIC_PORT), PublicPortalHandler); public_server.daemon_threads=True
        threading.Thread(target=public_server.serve_forever, daemon=True).start()
        threading.Thread(target=open_browser_later, daemon=True).start()
        try: server.serve_forever()
        finally:
            public_server.shutdown(); public_server.server_close(); server.server_close()
    except Exception as e:
        log_exception(e)
        # pythonw ile çalışırken de kullanıcıya anlaşılır mesaj ver.
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, f'Teknik Servis Pro başlatılamadı.\n\nAyrıntı: {e}\n\nLog: {LOG_DIR / "server-error.log"}', 'Teknik Servis Pro', 0x10)
        except Exception: pass
        raise

if __name__=='__main__': main()
