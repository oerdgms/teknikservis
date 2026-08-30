import os, sys, json, time, secrets, hashlib, hmac, shutil, threading, webbrowser, traceback
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from http.cookies import SimpleCookie
from pathlib import Path

APP_VERSION = '2.3.4'
PORT = int(os.environ.get('PORT', '8972'))
HOST = os.environ.get('HOST', '0.0.0.0')

# Kaynak ve kullanıcı verileri uygulama klasöründe tutulur.
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).resolve().parent
    RESOURCE_DIR = Path(getattr(sys, '_MEIPASS', APP_DIR))
else:
    APP_DIR = Path(__file__).resolve().parent
    RESOURCE_DIR = APP_DIR

DB_FILE = APP_DIR / 'db.json'
BACKUP_DIR = APP_DIR / 'backups'
LOG_DIR = APP_DIR / 'logs'
STATIC_DIR = RESOURCE_DIR if getattr(sys, 'frozen', False) else APP_DIR
INDEX_FILE = STATIC_DIR / 'index.html'
SESSIONS = {}
SESSION_TTL = 12 * 60 * 60


def empty_db():
    return {
        'version': 2.34,
        'serviceRecords': [], 'cashRecords': [], 'inventory': [], 'users': [],
        'settings': {
            'businessName': 'Sistem Bilgisayar Teknik Destek',
            'businessSubtitle': 'Bilgisayar & Donanım Onarım Servisi',
            'phone': '', 'email': '', 'address': '', 'taxOffice': '', 'taxNo': '',
            'defaultWarrantyDays': 90, 'logo': '', 'theme': 'blue'
        }
    }


def ensure_storage():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f'Arayüz dosyası bulunamadı: {INDEX_FILE}')
    if not DB_FILE.exists():
        candidate = RESOURCE_DIR / 'db.json'
        if candidate.exists(): shutil.copy2(candidate, DB_FILE)
        else: DB_FILE.write_text(json.dumps(empty_db(), ensure_ascii=False, indent=2), encoding='utf-8')


def normalize_db(raw):
    base = empty_db()
    if isinstance(raw, list):
        base['serviceRecords'] = raw
        return base
    raw = raw if isinstance(raw, dict) else {}
    out = {**base, **raw}
    for key in ('serviceRecords', 'cashRecords', 'inventory', 'users'):
        out[key] = raw.get(key) if isinstance(raw.get(key), list) else []
    settings = raw.get('settings') if isinstance(raw.get('settings'), dict) else {}
    out['settings'] = {**base['settings'], **settings}
    return out


def read_db():
    ensure_storage()
    return normalize_db(json.loads(DB_FILE.read_text(encoding='utf-8-sig')))


def write_db(data):
    ensure_storage()
    normalized = normalize_db(data)
    normalized['version'] = 2.34
    temp = DB_FILE.with_suffix('.json.tmp')
    temp.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temp, DB_FILE)
    return normalized


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


class Handler(SimpleHTTPRequestHandler):
    server_version = 'TeknikServisPro/2.3.4'

    def log_message(self, fmt, *args):
        try:
            with (LOG_DIR / 'access.log').open('a', encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {self.address_string()} {fmt % args}\n")
        except Exception: pass

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
            if p == '/api/auth/status':
                db = read_db(); u = session_user(self.headers)
                return self.send_json({'setupRequired': len(db['users']) == 0, 'authenticated': bool(u), 'user': u})
            if p == '/api/users':
                if not self.auth(admin=True): return
                return self.send_json([safe_user(x) for x in read_db()['users']])
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
            if p == '/api/data':
                if not self.auth(): return
                current=read_db(); nextdb=normalize_db(body); nextdb['users']=current['users']; backup_current_db(); write_db(nextdb)
                return self.send_json({'success':True})
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
        server=ThreadingHTTPServer((HOST, PORT), Handler)
        threading.Thread(target=open_browser_later, daemon=True).start()
        server.serve_forever()
    except Exception as e:
        log_exception(e)
        # pythonw ile çalışırken de kullanıcıya anlaşılır mesaj ver.
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, f'Teknik Servis Pro başlatılamadı.\n\nAyrıntı: {e}\n\nLog: {LOG_DIR / "server-error.log"}', 'Teknik Servis Pro', 0x10)
        except Exception: pass
        raise

if __name__=='__main__': main()
