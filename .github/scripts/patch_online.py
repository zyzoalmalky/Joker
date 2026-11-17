from pathlib import Path
R = Path('extracted/JOKER_V4_2')
P = R / 'worker/index.js'
s = P.read_text(encoding='utf-8')
old = 'cumulativeScores:g.cumulativeScores,finalScore:g.finalScore||null'
assert old in s
s = s.replace(old, 'cumulativeScores:g.cycleComplete?g.cumulativeScores:null,finalScore:g.finalScore||null', 1)
old = "async disconnect(sid){this.sessions.delete(sid);const p=this.playerFor(sid);if(p){p.connected=false;await this.persist();this.broadcast();}}"
 ew = "async disconnect(sid){this.sessions.delete(sid);const p=this.playerFor(sid);if(p){p.connected=false;if(this.room.hostId===p.id){const successor=this.room.players.find(x=>x.connected&&x.id!==p.id);if(successor)this.room.hostId=successor.id;}await this.persist();this.broadcast();}}"
assert old in s
s = s.replace(old, new, 1)
old = "if(this.room.players.length!==4)return this.send(this.sessions.get(p.sessionId),{type:'ERROR',message:'لازم يدخل 4 لاعبين قبل البداية.'});"
 ew = "if(this.room.players.length!==4||!this.room.players.every(x=>x.connected))return this.send(this.sessions.get(p.sessionId),{type:'ERROR',message:'لازم يدخل 4 لاعبين متصلين قبل البداية.'});"
assert old in s
s = s.replace(old, new, 1)
P.write_text(s.replace(old, new, 1), encoding='utf-8')
P = R / 'src/app.js'
s = P.read_text(encoding='utf-8')
old = "const $=id=>document.getElementById(id);let socket=null,seat=null,playerId=null,view=null,selected=null,pendingJoker=null,currentCode=null;"
 ew = "const $=id=>document.getElementById(id);let socket=null,seat=null,playerId=null,view=null,selected=null,pendingJoker=null,currentCode=null,reconnectTimer=null,reconnectDelay=1200,audioContext=null,lastTurnCount=null,lastPileCounts=null;"
assert old in s
s = s.replace(old, new, 1)
old = "function msg(t){const target=$('home').classList.contains('hidden')?$('notice'):$('status');target.textContent=t;}\n"
 ew = old + "function ensureAudio(){try{audioContext??=new (window.AudioContext||window.webkitAudioContext)();if(audioContext.state==='suspended')audioContext.resume();}catch{}}\nfunction tone(frequency,duration,wave='sine',volume=0.035,slide=0){if(!audioContext)return;const now=audioContext.currentTime,osc=audioContext.createOscillator(),gain=audioContext.createGain();osc.type=wave;osc.frequency.setValueAtTime(frequency,now);if(slide)osc.frequency.exponentialRampToValueAtTime(Math.max(1,frequency+slide),now+duration);gain.gain.setValueAtTime(volume,now);gain.gain.exponentialRampToValueAtTime(0.001,now+duration);osc.connect(gain);gain.connect(audioContext.destination);osc.start(now);osc.stop(now+duration);}\nfunction playTap(){tone(240,0.055,'triangle',0.045,-85);}\nfunction playShuffle(){tone(520,0.07,'sawtooth',0.018,-280);setTimeout(()=>tone(360,0.09,'triangle',0.022,-190),55);}\n"
assert old in s
s = s.replace(old, new, 1)
old = "currentCode=code;const token=type==='JOIN'?localStorage.getItem(`joker-token-${code}`):null;"
 ew = "currentCode=code;if(reconnectTimer){clearTimeout(reconnectTimer);reconnectTimer=null;}const token=type==='JOIN'?localStorage.getItem(`joker-token-${code}`):null;"
assert old in s
s = s.replace(old, new, 1)
old = "if(socket)try{socket.close();}catch{}socket=new WebSocket(`${base}/room/${code}`);socket.onopen=()=>socket.send(JSON.stringify({type,name,code,...(token?{playerToken:token}:{})}));socket.onmessage=e=>"
 ew = "if(socket)try{socket.close();}catch{}const ws=new WebSocket(`${base}/room/${code}`);socket=ws;ws.onopen=()=>{reconnectDelay=1200;ws.send(JSON.stringify({type,name,code,...(token?{playerToken:token}:{})}));};ws.onmessage=e=>"
assert old in s
s = s.replace(old, new, 1)
old = "if(m.type==='WELCOME'){playerId=m.playerId;"
 ew = "if(m.type==='WELCOME'){lastTurnCount=null;lastPileCounts=null;playerId=m.playerId;"
assert old in s
s = s.replace(old, new, 1)
old = "socket.onerror=()=>msg('تعذر الاتصال بالسيرفر. تأكد من تشغيل Worker.');socket.onclose=()=>{if(!$('table').classList.contains('hidden'))msg('انقطع الاتصال. يمكنك استعادة مقعدك من نفس الجهاز.');};"
 ew = "ws.onerror=()=>msg('تعذر الاتصال بالسيرفر. جاري محاولة إعادة الاتصال.');ws.onclose=()=>{if(socket!==ws)return;if(!$('table').classList.contains('hidden')&&currentCode){msg('انقطع الاتصال. جاري استعادة مقعدك تلقائيًا…');if(!reconnectTimer){reconnectTimer=setTimeout(()=>{reconnectTimer=null;connect('JOIN',true);reconnectDelay=Math.min(reconnectDelay*1.7,15000);},reconnectDelay);}};};"
assert old in s
s = s.replace(old, new, 1)
old = "if(g.turn!==seat)return msg('مش دورك.');if(c.joker){pendingJoker=c.id;"
 ew = "if(g.turn!==seat)return msg('مش دورك.');ensureAudio();if(c.joker){pendingJoker=c.id;"
assert old in s
s = s.replace(old, new, 1)
old = "})));$('start').classList.toggle('hidden',!g.cycleComplete"
 ew = "})));if(lastTurnCount!==null&&g.turnCount>lastTurnCount){const counts=g.piles.map(p=>p.length);if(lastPileCounts&&counts.some((n,i)=>n>lastPileCounts[i]))playShuffle();else playTap();}lastTurnCount=g.turnCount;lastPileCounts=g.piles.map(p=>p.length);$('start').classList.toggle('hidden',!g.cycleComplete"
assert old in s
s = s.replace(old, new, 1)
P.write_text(s.replace(old, new, 1), encoding='utf-8')
test_path = R / 'tests/room.test.js'
existing = test_path.read_text(encoding='utf-8')
tests = """

test('host role transfers to a connected player when the host disconnects', async()=>{
  const room=makeRoom(); await room.ready;
  const sockets=[];
  for(const i of [0,1,2,3]){const ws=fakeSocket();sockets.push(ws);const sid=`s${i}`;room.sessions.set(sid,ws);await room.join(sid,ws,{type:i===0?'CREATE':'JOIN',code:'ABC123',name:`P${i}`});}
  const oldHost=room.room.hostId;
  await room.disconnect('s0');
  assert.notEqual(room.room.hostId,oldHost);
  assert.equal(room.room.players.find(p=>p.id===room.room.hostId).connected,true);
  assert.equal(room.view(room.room.players[1].id).isHost,true);
});

test('a room cannot start while one of its four seats is disconnected', async()=>{
  const room=makeRoom(); await room.ready;
  const sockets=[];
  for(const i of [0,1,2,3]){const ws=fakeSocket();sockets.push(ws);const sid=`s${i}`;room.sessions.set(sid,ws);await room.join(sid,ws,{type:i===0?'CREATE':'JOIN',code:'ABC123',name:`P${i}`});}
  await room.disconnect('s3');
  await room.start(room.room.players[0]);
  assert.equal(room.room.started,false);
  assert.equal(sockets[0].sent.at(-1).type,'ERROR');
  assert.match(sockets[0].sent.at(-1).message,/4 لاعبين متصلين/);
});

test('cumulative scores are not exposed to clients until the cycle ends', async()=>{
  const room=makeRoom(); await room.ready;
  await room.join('s0',fakeSocket(),{type:'CREATE',code:'ABC123',name:'P0'});
  room.room.game={round:2,turn:0,dealerIndex:0,farsh:[],piles:[[],[],[],[]],hands:[[],[],[],[]],turnCount:0,cycleComplete:false,cumulativeScores:[120,90],dossaPending:null};
  assert.equal(room.view(room.room.players[0].id).game.cumulativeScores,null);
  room.room.game.cycleComplete=true;
  assert.deepEqual(room.view(room.room.players[0].id).game.cumulativeScores,[120,90]);
});
"""
if 'host role transfers to a connected player' not in existing:
  existing += tests
test_path.write_text(existing, encoding='utf-8')
print('Applied JOKER online reliability patch.')
