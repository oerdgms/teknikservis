const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const crypto = require('crypto');

const app = express();
const PORT = Number(process.env.PORT || 8972);
const HOST = process.env.HOST || '0.0.0.0';
const DB_FILE = path.join(__dirname, 'db.json');
const BACKUP_DIR = path.join(__dirname, 'backups');
const sessions = new Map();

app.use(cors({ origin: true, credentials: true }));
app.use(express.json({ limit: '10mb' }));

const emptyDb = () => ({
  version: 2.1,
  serviceRecords: [], cashRecords: [], inventory: [], users: [],
  settings: {
    businessName: 'Sistem Bilgisayar Teknik Destek',
    businessSubtitle: 'Bilgisayar & Donanım Onarım Servisi',
    phone: '', email: '', address: '', taxOffice: '', taxNo: '',
    defaultWarrantyDays: 90, logo: '', theme: 'blue'
  }
});

function ensureStorage() {
  if (!fs.existsSync(BACKUP_DIR)) fs.mkdirSync(BACKUP_DIR, { recursive: true });
  if (!fs.existsSync(DB_FILE)) fs.writeFileSync(DB_FILE, JSON.stringify(emptyDb(), null, 2), 'utf8');
}
function normalizeDb(raw) {
  const base = emptyDb();
  if (Array.isArray(raw)) return { ...base, serviceRecords: raw };
  return {
    ...base, ...(raw || {}),
    serviceRecords: Array.isArray(raw?.serviceRecords) ? raw.serviceRecords : [],
    cashRecords: Array.isArray(raw?.cashRecords) ? raw.cashRecords : [],
    inventory: Array.isArray(raw?.inventory) ? raw.inventory : [],
    users: Array.isArray(raw?.users) ? raw.users : [],
    settings: { ...base.settings, ...(raw?.settings || {}) }
  };
}
function readDb(){ ensureStorage(); return normalizeDb(JSON.parse(fs.readFileSync(DB_FILE,'utf8'))); }
function writeDb(data){ ensureStorage(); const normalized=normalizeDb(data); normalized.version=2.21; const temp=DB_FILE+'.tmp'; fs.writeFileSync(temp,JSON.stringify(normalized,null,2),'utf8'); fs.renameSync(temp,DB_FILE); return normalized; }
function backupCurrentDb(){ if(!fs.existsSync(DB_FILE)) return; const stamp=new Date().toISOString().replace(/[:.]/g,'-'); fs.copyFileSync(DB_FILE,path.join(BACKUP_DIR,`db_${stamp}.json`)); const files=fs.readdirSync(BACKUP_DIR).filter(x=>x.endsWith('.json')).sort().reverse(); files.slice(20).forEach(f=>{try{fs.unlinkSync(path.join(BACKUP_DIR,f))}catch(_){}}); }
function hashPassword(password,salt=crypto.randomBytes(16).toString('hex')){ const hash=crypto.scryptSync(String(password),salt,64).toString('hex'); return `${salt}:${hash}`; }
function verifyPassword(password,stored=''){ const [salt,hash]=String(stored).split(':'); if(!salt||!hash)return false; const calc=crypto.scryptSync(String(password),salt,64); const saved=Buffer.from(hash,'hex'); return saved.length===calc.length && crypto.timingSafeEqual(saved,calc); }
function parseCookies(req){ return Object.fromEntries(String(req.headers.cookie||'').split(';').map(x=>x.trim()).filter(Boolean).map(x=>{const i=x.indexOf('=');return [decodeURIComponent(x.slice(0,i)),decodeURIComponent(x.slice(i+1))]})); }
function sessionUser(req){ const token=parseCookies(req).tsp_session; if(!token)return null; const s=sessions.get(token); if(!s||s.expires<Date.now()){ if(token)sessions.delete(token); return null; } s.expires=Date.now()+12*60*60*1000; return s.user; }
function setSession(res,user){ const token=crypto.randomBytes(32).toString('hex'); sessions.set(token,{user:{id:user.id,name:user.name,username:user.username,role:user.role},expires:Date.now()+12*60*60*1000}); res.setHeader('Set-Cookie',`tsp_session=${token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=43200`); }
function requireAuth(req,res,next){ const u=sessionUser(req); if(!u)return res.status(401).json({error:'Oturum gerekli'}); req.user=u; next(); }
function requireAdmin(req,res,next){ if(req.user?.role!=='Yönetici')return res.status(403).json({error:'Yönetici yetkisi gerekli'}); next(); }
function publicData(db){ const {users,...safe}=db; return safe; }

app.get('/api/health',(_req,res)=>res.json({ok:true,version:'2.2.1'}));
app.get('/api/auth/status',(req,res)=>{ const db=readDb(); const u=sessionUser(req); res.json({setupRequired:db.users.length===0,authenticated:!!u,user:u||null}); });
app.post('/api/auth/setup',(req,res)=>{ const db=readDb(); if(db.users.length)return res.status(409).json({error:'İlk kurulum tamamlanmış'}); const name=String(req.body.name||'').trim(), username=String(req.body.username||'').trim(), password=String(req.body.password||''); if(!name||username.length<3||password.length<6)return res.status(400).json({error:'Ad, en az 3 karakter kullanıcı adı ve en az 6 karakter şifre gerekli'}); const user={id:Date.now(),name,username,role:'Yönetici',active:true,passwordHash:hashPassword(password),createdAt:new Date().toISOString()}; db.users.push(user); backupCurrentDb(); writeDb(db); setSession(res,user); res.json({success:true,user:{id:user.id,name:user.name,username:user.username,role:user.role}}); });
app.post('/api/auth/login',(req,res)=>{ const db=readDb(); const username=String(req.body.username||'').trim().toLocaleLowerCase('tr-TR'); const user=db.users.find(x=>x.active!==false&&String(x.username).toLocaleLowerCase('tr-TR')===username); if(!user||!verifyPassword(req.body.password,user.passwordHash))return res.status(401).json({error:'Kullanıcı adı veya şifre hatalı'}); setSession(res,user); res.json({success:true,user:{id:user.id,name:user.name,username:user.username,role:user.role}}); });
app.post('/api/auth/logout',(req,res)=>{ const token=parseCookies(req).tsp_session; if(token)sessions.delete(token); res.setHeader('Set-Cookie','tsp_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0'); res.json({success:true}); });
app.post('/api/auth/change-password',requireAuth,(req,res)=>{ const db=readDb(), user=db.users.find(x=>x.id===req.user.id); if(!user||!verifyPassword(req.body.currentPassword,user.passwordHash))return res.status(400).json({error:'Mevcut şifre yanlış'}); const np=String(req.body.newPassword||''); if(np.length<6)return res.status(400).json({error:'Yeni şifre en az 6 karakter olmalı'}); user.passwordHash=hashPassword(np); backupCurrentDb(); writeDb(db); res.json({success:true}); });
app.get('/api/users',requireAuth,requireAdmin,(req,res)=>{ const db=readDb(); res.json(db.users.map(({passwordHash,...u})=>u)); });
app.post('/api/users',requireAuth,requireAdmin,(req,res)=>{ const db=readDb(); const name=String(req.body.name||'').trim(), username=String(req.body.username||'').trim(), password=String(req.body.password||''), role=['Yönetici','Teknisyen','Kasa'].includes(req.body.role)?req.body.role:'Teknisyen'; if(!name||username.length<3||password.length<6)return res.status(400).json({error:'Bilgileri kontrol edin; şifre en az 6 karakter olmalı'}); if(db.users.some(x=>String(x.username).toLocaleLowerCase('tr-TR')===username.toLocaleLowerCase('tr-TR')))return res.status(409).json({error:'Bu kullanıcı adı zaten kullanılıyor'}); db.users.push({id:Date.now(),name,username,role,active:true,passwordHash:hashPassword(password),createdAt:new Date().toISOString()}); backupCurrentDb(); writeDb(db); res.json({success:true}); });
app.patch('/api/users/:id',requireAuth,requireAdmin,(req,res)=>{ const db=readDb(), user=db.users.find(x=>String(x.id)===req.params.id); if(!user)return res.status(404).json({error:'Kullanıcı bulunamadı'}); if(user.id===req.user.id && req.body.active===false)return res.status(400).json({error:'Kendi hesabınızı pasif yapamazsınız'}); if(req.body.name!=null)user.name=String(req.body.name).trim()||user.name; if(['Yönetici','Teknisyen','Kasa'].includes(req.body.role))user.role=req.body.role; if(req.body.active!=null)user.active=!!req.body.active; if(String(req.body.password||'').length>=6)user.passwordHash=hashPassword(req.body.password); backupCurrentDb(); writeDb(db); res.json({success:true}); });

app.get('/api/data',requireAuth,(_req,res)=>{ try{res.json(publicData(readDb()))}catch(err){console.error(err);res.status(500).json({error:'Veri okuma hatası'})} });
app.post('/api/data',requireAuth,(req,res)=>{ try{ backupCurrentDb(); const current=readDb(); const next=normalizeDb({...req.body,users:current.users}); writeDb(next); res.json({success:true}); }catch(err){console.error(err);res.status(500).json({error:'Veri yazma hatası'})} });

app.use(express.static(__dirname));
app.use((err,_req,res,_next)=>{console.error(err);res.status(500).json({error:'Sunucu hatası'})});
ensureStorage();
app.listen(PORT,HOST,()=>{ console.log('===================================================='); console.log('Sistem Bilgisayar Teknik Servis Pro v2.2.1 çalışıyor'); console.log(`Bu bilgisayardan: http://localhost:${PORT}`); console.log(`Yerel ağdan: http://[BILGISAYAR-IP]:${PORT}`); console.log('===================================================='); });
